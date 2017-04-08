# piazza_bot
Piazza bot that indexes all posts and enables quick searches on them

## Usage

```
git clone https://github.com/pranavr93/piazza_bot.git
cd piazza_bot/
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

You are all set up. Run the below code
```
python index.py <search_term1> <search_term2> ...
```

Note:
* Running the above command for the first time could take time due to indexing
* If index is present, it should perform quick searches of the query terms
* Search is done on the contents of the post
* An "OR" query is performed on the query terms
