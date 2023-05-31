package main

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"strings"

	"github.com/google/go-github/v52/github"
	"golang.org/x/oauth2"
)

func main() {
	token := os.Getenv("APP_TOKEN")
	if token == "" {
		fmt.Println("APP_TOKEN is not set")
		return
	}

	ctx := context.Background()
	ts := oauth2.StaticTokenSource(
		&oauth2.Token{AccessToken: token},
	)
	tc := oauth2.NewClient(ctx, ts)

	client := github.NewClient(tc)

	repoName := os.Getenv("REPONAME")
	if repoName == "" {
		fmt.Println("REPONAME is not set")
		return
	}

	searchTerm := fmt.Sprintf("github.com/%s", repoName)
	query := fmt.Sprintf("org:remerge filename:go.mod %s", searchTerm)
	searchOptions := &github.SearchOptions{
		ListOptions: github.ListOptions{PerPage: 100},
		TextMatch:   true,
	}

	dependants := []string{}

	for {
		result, response, err := client.Search.Code(ctx, query, searchOptions)
		if err != nil {
			fmt.Printf("Error searching code: %v\n", err)
			return
		}

		for _, file := range result.CodeResults {
			for _, match := range file.TextMatches {
				lines := strings.Split(*match.Fragment, "\n")
				for _, line := range lines {
					// exclude reference to self and any indirect dependencies
					if strings.Contains(line, searchTerm) && !strings.Contains(line, fmt.Sprintf("module %s", searchTerm)) && !strings.Contains(line, "// indirect") {
						dependants = append(dependants, *file.Repository.Name)
					}
				}
			}
		}

		if response.NextPage == 0 {
			break
		}
		searchOptions.Page = response.NextPage
	}

	j, err := json.Marshal(dependants)
	if err != nil {
		fmt.Printf("Error: %s", err.Error())
	} else {
		fmt.Println(string(j))
	}
}
