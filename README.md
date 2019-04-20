# github-trending-repo
To mail daily/weekly/monthly trending repository from Github


I usually like to see what's trending in the Github. The problem is that most of the trending repositories are repetitive and I only want to see _delta_(new repositories


What does this project do:

1. I am using https://github.com/huchenme/github-trending-api to fetch Github's trending repositories.

2. It will store that information in **AWS DynamoDB** table

  Sample record:

        {
          "added_on": "2019-04-19 21:30:22",
          "description": "All Algorithms implemented in Java",
          "language": "java",
          "name": "Java",
          "url": "https://github.com/TheAlgorithms/Java"
        }

3. I am only interested in repositories with README and description in English. I use **AWS Comprehend** to check the language of the text and filter our non-English stuff.

4. I fetch new trending repositories and find delta after comparing it with existing DynamoDB data. Then, I use AWS SNS to push this data to a topic. I subscribed to that topic via email.
