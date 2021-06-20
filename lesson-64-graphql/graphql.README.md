
Learn GraphQL in 40 mins
https://www.youtube.com/watch?v=ZQL7tL2S0oQ&t=1934s


## Install 
```
$ sudo npm install -g npm
$ sudo npm install -g --force nodemon  # fix nodemon command not found

$ npm init

$ npm i express express-graphql graphql  # install graphql pkgs

$ npm audit fix  --force  # fix high risk items

$ npm i --save-dev nodemon  # great for dev without restart

$ nodemon server.js  # launch server at http://localhost:5000/graphql

```

## How to use graphql API


```
# title = Learn GraphQL in 40 mins 
# video = https://www.youtube.com/watch?v=ZQL7tL2S0oQ&t=1934s
# src = https://github.com/WebDevSimplified/Learn-GraphQL.git
# src = https://github.com/wgong/Learn-GraphQL

# title = modern-graphql-tutorial
# src = https://github.com/wgong/modern-graphql-tutorial


# title = A Brief Tour of GraphQL
# blog = https://dev.to/mychal/a-brief-tour-of-graphql-4lcg

### query a single book
query  get_single_book  {
  book(id:4) {
    id
  	name   # book title
    author {
      id
      name
    }
  }
}

query  get_single_book2  {
  book(id:9) {
    id
  	name   # book title
    author {
      id
      name
    }
  }
}

### query a list of all books with title and author name
query  get_books  {
  books {
    id
  	name 
    author {
      id
      name
    }
  }
}

### get an author
query get_an_author {
  author(id:2) {
    id
    name
  }
  
}

### query a list of authors with their books
query get_an_author_with_books {
  author(id:2) {
    id
    name
    books {
      id
      name
    }
  }
  
}

### query all authors
query get_authors {
  authors {
    id
    name
  }
  
}

### add author
mutation add_an_author {
  addAuthor (
    name: "Matei Zaharia"
  ) {
    name
  }
}

### add book
mutation add_a_book {
  addBook (
    name: "Spark - The definite Guide"
    authorId: 4
  ) {
    name
    authorId
  }
}

```

## Javascript resource

### online editor - playcode.io

https://playcode.io/


