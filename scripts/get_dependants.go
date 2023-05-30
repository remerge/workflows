package main

import (
	"context"
	"encoding/json"
	"fmt"
	"os"

	"github.com/google/go-github/v52/github"
	"golang.org/x/oauth2"
)

func main() {
	ctx := context.Background()
	ts := oauth2.StaticTokenSource(
		&oauth2.Token{AccessToken: os.Getenv("APP_TOKEN")},
	)
	tc := oauth2.NewClient(ctx, ts)

	client := github.NewClient(tc)

	repoName := os.Getenv("REPONAME")
	query := fmt.Sprintf("org:remerge filename:go.mod github.com/%s", repoName)
	searchOptions := &github.SearchOptions{
		ListOptions: github.ListOptions{PerPage: 100},
	}

	dependants := []string{}

	for {
		result, response, err := client.Search.Code(ctx, query, searchOptions)
		if err != nil {
			fmt.Printf("Error searching code: %v\n", err)
			return
		}

		for _, file := range result.CodeResults {
			dependants = append(dependants, *file.Repository.Name)
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
