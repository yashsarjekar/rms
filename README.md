# SETUP

```
python -m venv venv
source venv/bin/activate
git clone https://github.com/yashsarjekar/rms.git
cd rms
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
Create Super User
python manage.py runserver
```

## ENDPOINT
```
http://ec2-13-233-57-139.ap-south-1.compute.amazonaws.com:8000/api/token/
http://ec2-13-233-57-139.ap-south-1.compute.amazonaws.com:8000/graphql/
```



## GENERATE TOKEN
```
curl --location 'http://ec2-13-233-57-139.ap-south-1.compute.amazonaws.com:8000/api/token/' \
--header 'Content-Type: application/json' \
--data '{
    "username": "yash",
    "password": "yash"
}'
```

### RESPONSE
```
{
    "token": "dsdkdlkdslkdskldskdssdklkslldskdlds"
}
```




## CREATE INGREDIENT
```
mutation {
    createIngredient(name: "Milk powder", description: "Fresh Milk") {
      ingredient {
        id
        name
        description
      }
    }
}
```

### cURL
```
curl --location 'http://ec2-13-233-57-139.ap-south-1.compute.amazonaws.com:8000/graphql/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token dsdkdlkdslkdskldskdssdklkslldskdlds' \
--header 'Cookie: csrftoken=JdtD69L5acrCI4PKTKGj4blVlFGIDn5W' \
--data '{"query":"mutation {\n    createIngredient(name: \"Tea powder\", description: \"Fresh Tea\") {\n      ingredient {\n        id\n        name\n        description\n      }\n    }\n}","variables":{}}'
```

### RESPONSE
```
{
    "data": {
        "createIngredient": {
            "ingredient": {
                "id": "6",
                "name": "Tea powder",
                "description": "Fresh Tea"
            }
        }
    }
}
```


## UPDATE INGREDIENT
```
mutation {
    updateIngredient(id: 2, name: "Milk pow", description: "Fresh Milk only ") {
      ingredient {
        id
        name
        description
      }
    }
}
```

### cURL
```
curl --location 'http://ec2-13-233-57-139.ap-south-1.compute.amazonaws.com:8000/graphql/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token dsdkdlkdslkdskldskdssdklkslldskdlds' \
--header 'Cookie: csrftoken=JdtD69L5acrCI4PKTKGj4blVlFGIDn5W' \
--data '{"query":"mutation {\n    updateIngredient(id: 2, name: \"Milk powd\", description: \"Fresh Milk only \") {\n      ingredient {\n        id\n        name\n        description\n      }\n    }\n}","variables":{}}'
```

### RESPONSE
```
{
    "data": {
        "updateIngredient": {
            "ingredient": {
                "id": "2",
                "name": "Milk powd",
                "description": "Fresh Milk only"
            }
        }
    }
}
```



## DELETE INGREDIENT
```
mutation {
    deleteIngredient(id: 2) {
       success
    }
}
```

### cURL
```
curl --location 'http://ec2-13-233-57-139.ap-south-1.compute.amazonaws.com:8000/graphql/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token dsdkdlkdslkdskldskdssdklkslldskdlds' \
--header 'Cookie: csrftoken=JdtD69L5acrCI4PKTKGj4blVlFGIDn5W' \
--data '{"query":"mutation {\n    deleteIngredient(id: 3) {\n       success\n    }\n}","variables":{}}'
```
### RESPONSE
```
{
    "data": {
        "deleteIngredient": {
            "success": true
        }
    }
}
```



## SEARCH INGREDIENT 
```
query MyQuery {
  allIngredients(page: 1, pageSize: 2, search: "Potato") {
   ingredients {
      id
      name
      description
    }
    totalPages
    hasNextPage
  }
}
```

### cURL
```
curl --location 'http://ec2-13-233-57-139.ap-south-1.compute.amazonaws.com:8000/graphql/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token dsdkdlkdslkdskldskdssdklkslldskdlds' \
--header 'Cookie: csrftoken=JdtD69L5acrCI4PKTKGj4blVlFGIDn5W' \
--data '{"query":"query MyQuery {\n  allIngredients(page: 1, pageSize: 2, search: \"Potato\") {\n   ingredients {\n      id\n      name\n      description\n    }\n    totalPages\n    hasNextPage\n  }\n}","variables":{}}'
```

### RESPONSE
```
{
    "data": {
        "allIngredients": {
            "ingredients": [
                {
                    "id": "1",
                    "name": "Potato",
                    "description": "Fresh Potato only "
                }
            ],
            "totalPages": 1,
            "hasNextPage": false
        }
    }
}
```



## PAGINATION OF INGREDIENT
```
query MyQuery {
  allIngredients(page: 2, pageSize: 1) {
   ingredients {
      id
      name
      description
    }
    totalPages
    hasNextPage
  }
}
```

### cURL
```
curl --location 'http://ec2-13-233-57-139.ap-south-1.compute.amazonaws.com:8000/graphql/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token dsdkdlkdslkdskldskdssdklkslldskdlds' \
--header 'Cookie: csrftoken=JdtD69L5acrCI4PKTKGj4blVlFGIDn5W' \
--data '{"query":"query MyQuery {\n  allIngredients(page: 2, pageSize: 1) {\n   ingredients {\n      id\n      name\n      description\n    }\n    totalPages\n    hasNextPage\n  }\n}","variables":{}}'
```

### RESPONSE
```
{
    "data": {
        "allIngredients": {
            "ingredients": [
                {
                    "id": "4",
                    "name": "Milk",
                    "description": "Fresh Milk only"
                }
            ],
            "totalPages": 5,
            "hasNextPage": true
        }
    }
}
```


## CREATE RECIPE
```
mutation {
  createRecipe(
    instructions: "Add ingredient Milk Potato Tomato"
    title: "Milk Tomato Potato"
    ingredients: [1, 2,3, 4]
  ) {
    recipe {
      id
      ingredients {
        description
        id
        name
      }
      instructions
      title
    }
  }
}
```

### cURL
```
curl --location 'http://ec2-13-233-57-139.ap-south-1.compute.amazonaws.com:8000/graphql/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token dsdkdlkdslkdskldskdssdklkslldskdlds' \
--header 'Cookie: csrftoken=JdtD69L5acrCI4PKTKGj4blVlFGIDn5W' \
--data '{"query":"mutation {\n  createRecipe(\n    instructions: \"Add ingredient Milk Potato Tomato\"\n    title: \"Milk Tomato Potato\"\n    ingredients: [1,2]\n  ) {\n    recipe {\n      id\n      ingredients {\n        description\n        id\n        name\n      }\n      instructions\n      title\n    }\n  }\n}","variables":{}}'
```

### RESPONSE
```
{
    "data": {
        "createRecipe": {
            "recipe": {
                "id": "6",
                "ingredients": [
                    {
                        "description": "Fresh Potato only ",
                        "id": "1",
                        "name": "Potato"
                    },
                    {
                        "description": "Fresh Milk only",
                        "id": "2",
                        "name": "Milk powd"
                    }
                ],
                "instructions": "Add ingredient Milk Potato Tomato",
                "title": "Milk Tomato Potato"
            }
        }
    }
}
```


## FETCH RECIPE BY ID
```
query MyQuery {
  recipeById(id: "1") {
    ingredients {
      description
      id
      name
    }
    ingredientCount
    id
    instructions
    title
  }
}
```

### cURL
```
curl --location 'http://ec2-13-233-57-139.ap-south-1.compute.amazonaws.com:8000/graphql/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token 8d02feb88d72fb94ca530540429a7c308315a1ed' \
--header 'Cookie: csrftoken=JdtD69L5acrCI4PKTKGj4blVlFGIDn5W' \
--data '{"query":"query MyQuery {\n  recipeById(id: \"1\") {\n    ingredients {\n      description\n      id\n      name\n    }\n    ingredientCount\n    id\n    instructions\n    title\n  }\n}","variables":{}}'
```

### RESPONSE
```
{
    "data": {
        "recipeById": {
            "ingredients": [
                {
                    "description": "Fresh Milk only",
                    "id": "2",
                    "name": "Milk powd"
                }
            ],
            "ingredientCount": 1,
            "id": "1",
            "instructions": "Add ingredient Potato Tomato",
            "title": "Tomato Chatni"
        }
    }
}
```


## ADD INGREDIENT TO RECIPE
```
mutation MyMutation {
  addIngredientInRecipe(id: "1", ingredients: [5]) {
    recipe {
      id
      instructions
      ingredients {
        description
        id
        name
      }
      title
    }
  }
}
```

### cURL
```
curl --location 'http://ec2-13-233-57-139.ap-south-1.compute.amazonaws.com:8000/graphql/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token 8d02feb88d72fb94ca530540429a7c308315a1ed' \
--header 'Cookie: csrftoken=JdtD69L5acrCI4PKTKGj4blVlFGIDn5W' \
--data '{"query":"mutation MyMutation {\n  addIngredientInRecipe(id: \"1\", ingredients: [5]) {\n    recipe {\n      id\n      instructions\n      ingredients {\n        description\n        id\n        name\n      }\n      title\n    }\n  }\n}","variables":{}}'
```

### RESPONSE
```
{
    "data": {
        "addIngredientInRecipe": {
            "recipe": {
                "id": "1",
                "instructions": "Add ingredient Potato Tomato",
                "ingredients": [
                    {
                        "description": "Fresh Milk",
                        "id": "5",
                        "name": "Milk powder"
                    },
                    {
                        "description": "Fresh Milk only",
                        "id": "2",
                        "name": "Milk powd"
                    }
                ],
                "title": "Tomato Chatni"
            }
        }
    }
}
```

## DELETE INGREDIENT FROM RECIPE
```
mutation MyMutation {
  deleteIngredientFromRecipe(id: 1, ingredients: [2]) {
    success
  }
}
```

### cURL
```
curl --location 'http://ec2-13-233-57-139.ap-south-1.compute.amazonaws.com:8000/graphql/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Token 8d02feb88d72fb94ca530540429a7c308315a1ed' \
--header 'Cookie: csrftoken=JdtD69L5acrCI4PKTKGj4blVlFGIDn5W' \
--data '{"query":"mutation MyMutation {\n  deleteIngredientFromRecipe(id: 1, ingredients: [2]) {\n    success\n  }\n}","variables":{}}'
```
 
### RESPONSE
```
{
    "data": {
        "deleteIngredientFromRecipe": {
            "success": true
        }
    }
}
```
