import requests
import pandas as pd
import time
import matplotlib.pyplot as plt


class HackerNewsData:
    def __init__(self):
        self.base_url = "https://hacker-news.firebaseio.com/v0/"
        self.top_stories_url = self.base_url + "topstories.json"
        self.item_url = self.base_url + "item/{}.json"
        self.stories = []


    def fetch_top_stories(self, limit = 5):
        response = requests.get(self.top_stories_url)
        if response.status_code == 200:
            top_stories_ids = response.json()[:limit]
            for story_id in top_stories_ids:
                story_details = self.fetch_item_details(story_id)
                if story_details:
                    self.stories.append(story_details)
                    time.sleep(0.5) 
        else:
            print("Failed to fetch top stories")


    def fetch_item_details(self, item_id):
        response = requests.get(self.item_url.format(item_id))
        if response.status_code == 200:
            return response.json()
        return None


    def save_stories_to_csv(self, filename="top_stories.csv"):
        df = pd.DataFrame(self.stories)
        df.to_csv(filename, index=False)
        print(f"Saved top stories to {filename}")


if __name__ == "__main__":
    hn_data = HackerNewsData()
    hn_data.fetch_top_stories(limit=5)
    hn_data.save_stories_to_csv("top_stories.csv")
 




class HackerNewsComments:
    def __init__(self):
        self.base_url = "https://hacker-news.firebaseio.com/v0/"
        self.item_url = self.base_url + "item/{}.json"
        self.comments = []


    def fetch_comments_for_stories(self, stories, limit_per_story = 15):
        for story in stories:
            if 'kids' in story:
                comment_ids = story['kids'][:limit_per_story]
                for comment_id in comment_ids:
                    comment_details = self.fetch_item_details(comment_id)
                    if comment_details:
                        comment_details['story_id'] = story['id']  
                        if not self.is_duplicate(comment_details):
                            self.comments.append(comment_details)
                            time.sleep(0.5)  
                        
                                    
    def fetch_item_details(self, item_id):
        response = requests.get(self.item_url.format(item_id))
        if response.status_code == 200:
            return response.json()
        return None


    def save_comments_to_csv(self, filename="comments.csv"):
        df = pd.DataFrame(self.comments)
        df.to_csv(filename, index=False)
        print(f"Saved comments to {filename}")
   
   
    def is_duplicate(self, comment_details):
        for comment in self.comments:
            if comment['id'] == comment_details['id']:
                return True
        return False  


if __name__ == "__main__":
    stories_df = pd.read_csv("top_stories.csv")
    stories = stories_df.to_dict('records')


    hn_comments = HackerNewsComments()
    hn_comments.fetch_comments_for_stories(stories, limit_per_story=15)
    hn_comments.save_comments_to_csv("comments.csv")



class HackerNewsAnalysis:
    def __init__(self, stories_file="top_stories.csv", comments_file="comments.csv"):
        self.stories_df = pd.read_csv(stories_file)
        self.comments_df = pd.read_csv(comments_file)


    def generate_summary_statistics(self):
        summary = {
            "average_score": self.stories_df['score'].mean(),
            "average_comments": self.stories_df['descendants'].mean(),
            "total_stories": len(self.stories_df),
            "total_comments": len(self.comments_df)
        }
        summary_df = pd.DataFrame([summary])
        summary_df.to_csv("summary_statistics.csv", index=False)
        print("Saved summary statistics to summary_statistics.csv")


    def plot_data(self):
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        self.stories_df['score'].plot(kind='hist', bins=20, color='skyblue')
        plt.title('Distribution of Story Scores')
        plt.xlabel('Score')
        plt.subplot(1, 2, 2)
        self.stories_df['descendants'].plot(kind='hist', bins=20, color='lightgreen')
        plt.title('Distribution of Number of Comments')
        plt.xlabel('Number of Comments')
        plt.tight_layout()
        plt.savefig("analysis_plots.png")
        plt.show()
        print("Saved plots to analysis_plots.png")


if __name__ == "__main__":
    hn_analysis = HackerNewsAnalysis()
    hn_analysis.generate_summary_statistics()
    hn_analysis.plot_data()
