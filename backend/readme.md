
# Backend API
## register
**request url:** /register \
**request type:** POST \
**request body:**
| name | type |
| :-----------: | :-------------:| 
| username       |   string      | 
| password       |   string      | 
| email       |   string      | 

**sample request body:**
{
    "username":"xxx", 
    "password":"123456", 
    "email":"xxx@abc.com"
} 

## log in
**request url:** /login \
**request type:** POST \
**request parameter:**
| name | type |
| :-----------: | :-------------:| 
| email       |   string      | 
| password       |   string      | 

**sample request body:**
{
    "email":"xxx@abc.com",
    "password":"123456"
} 

**response parameter:**
| name | type |
| :-----------: | :-------------:| 
| email       |   string      | 
| username       |   string      |
| userId       |   int      |


## change password
**request url:** /change_password \
**request type:** POST \
**request body:**
| name | type |
| :-----------: | :-------------:| 
| userId       |   int      | 
| new_password       |   string      | 

**sample request body:**
{
    "userId": 1, 
    "new_password":"123654"
} 

## delete account
**request url:** /delete_account \
**request type:** POST \
**request body:**
| name | type |
| :-----------: | :-------------:| 
| userId      |   int      | 

**sample request body:**
{
    "userId": 1
} 

## search
**request url:** /search \
**request type:** POST \
**request parameter:**
| name | type |
| :-----------: | :-------------:| 
| type       |   string      | 
| query       |   string      | 
| page       |   int      | 

**supported type:** mammal, country, continent, institution, publication \
**page:** zero indexed, always return the last page if exeeds the maximum amount

**response parameter:**
| name | type | description |
| :-----------: | :-------------:| :-------------:|
| dataList       |   list      |  record list for one page |
| count       |   int      | the number of all statisfied records |

## favor
**request url:** /favor \
**request type:** POST \
**request body:**
| name | type |
| :-----------: | :-------------:| 
| action       |   string      | 
| userId       |   int      | 
| mammalName       |   string      | 

**sample request body:**
{
    "action":"add", 
    "userId":1,
    "mammalId": "pandas"
} 

**supported action:** add and delete

## get favor
**request url:** /get_favor \
**request type:** POST \
**request parameter:**
| name | type |
| :-----------: | :-------------:| 
| userId       |   int      | 
| page       |   int      |

**response parameter:**
| name | type | description |
| :-----------: | :-------------:| :-------------:|
| dataList       |   list      |  record list for one page |
| count       |   int      | the number of all statisfied records |

## statistic
**request url:** /statistic \
**request type:** POST \
**request parameter:**
| name | type |
| :-----------: | :-------------:| 
| type       |   int      | 
| page       |   int      | 

**response parameter:**
| name | type | description |
| :-----------: | :-------------:| :-------------:|
| dataList       |   list      |  record list for one page |
| count       |   int      | the number of all statisfied records |
