import {backendLookup} from '../lookup'

export function apiTweetCreate(newTweet, callback){
    backendLookup("POST", "/tweets/create/", callback, {content: newTweet})
  }

export function apiTweetAction(tweetId, action, callback){
    const data = {id: tweetId, action: action}
    backendLookup("POST", "/tweets/action/", callback, data)
}

export function apiTweetDetial(tweetId, callback) {
    backendLookup("GET", `/tweets/${tweetId}/`, callback)
}


export function apiTweetList(username, callback) {
    let endpoint =  "/tweets/"
    if (username){
        endpoint =  `/tweets/?username=${username}`
    }
    backendLookup("GET", endpoint, callback)
}