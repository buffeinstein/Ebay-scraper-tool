

 The python file 'ebay-dl2.py' allows you to scrape ebay to find the following information about an item: 
1) name 
2) price
3) shipping cost
4) free return status
5) items sold
6) owned status 

When you run the file in your terminal, you may enter in three arguments. 

The arguments allow you to edit: 
1) what item you want to search for. make sure to put quotes around your item if the search has a space in it. EX: 'leather jacket women'. 
2) (optional argument, default set to 10 )enter in how many pages of ebay you want it to scrape with: --page_number = 
3) (optional argument, default set to json) enter in --csv if you want it saved as a csv file 

Here are the 6 commands I ran. All of them scrape 10 ebay pages, since I didn't specify a page number. 

The first three create json files.

```
/usr/local/bin/python3 /Users/ambikatiwari/Downloads/CS40/week9/project3/ebay-dl2.py 'leather jacket women'      
```

```
/usr/local/bin/python3 /Users/ambikatiwari/Downloads/CS40/week9/project3/ebay-dl2.py 'washi tape'      
```

```
/usr/local/bin/python3 /Users/ambikatiwari/Downloads/CS40/week9/project3/ebay-dl2.py 'fountain pen'      
```

The next three create csv files. 

```
/usr/local/bin/python3 /Users/ambikatiwari/Downloads/CS40/week9/project3/ebay-dl2.py 'leather jacket women' --csv
```

```
/usr/local/bin/python3 /Users/ambikatiwari/Downloads/CS40/week9/project3/ebay-dl2.py 'washi tape'   --csv
```

``` 
/usr/local/bin/python3 /Users/ambikatiwari/Downloads/CS40/week9/project3/ebay-dl2.py 'fountain pen'   --csv
```

Happy scraping!

This project was made to follow the instructions found  [here](https://github.com/mikeizbicki/cmc-csci040/tree/2022fall/project_03)





