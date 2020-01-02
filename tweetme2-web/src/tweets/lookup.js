import {backendLookup} from '../lookup'

export function apiTweetCreate(newTweet, callback){
    backendLookup("POST", "/tweets/create/", callback, {content: newTweet})
  }
  
export function apiTweetList(callback) {
    backendLookup("GET", "/tweets/", callback)
}