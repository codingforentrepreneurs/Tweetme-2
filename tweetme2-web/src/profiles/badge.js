import React, {useEffect, useState} from 'react'

import {UserDisplay, UserPicture} from './components'
import {apiProfileDetail, apiProfileFollowToggle} from './lookup'

import {DisplayCount} from './utils'

function ProfileBadge(props) {
    const {user, didFollowToggle, profileLoading} = props
    let currentVerb = (user && user.is_following) ? "Unfollow" : "Follow"
    currentVerb = profileLoading ? "Loading..." : currentVerb
    const handleFollowToggle = (event) => {
        event.preventDefault()
        if (didFollowToggle && !profileLoading) {
            didFollowToggle(currentVerb)
        }
    }
    return user ? <div>
        <UserPicture user={user} hideLink />
        <p><UserDisplay user={user} includeFullName hideLink /></p>
        <p><DisplayCount>{user.follower_count}</DisplayCount> {user.follower_count === 1 ? "follower" : "followers"} </p>
        <p><DisplayCount>{user.following_count}</DisplayCount> following</p>
        <p>{user.location}</p>
        <p>{user.bio}</p>
        <button className='btn btn-primary' onClick={handleFollowToggle}>{currentVerb}</button>
    </div> : null
}

export function ProfileBadgeComponent (props) {
    const {username} = props
    // lookup
    const [didLookup, setDidLookup] = useState(false)
    const [profile, setProfile] = useState(null)
    const [profileLoading, setProfileLoading] = useState(false)
    const handleBackendLookup = (response, status) => {
      if (status === 200) {
        setProfile(response)
      }
    }
    useEffect(()=>{
      if (didLookup === false){
        apiProfileDetail(username, handleBackendLookup)
        setDidLookup(true)
      }
    }, [username, didLookup, setDidLookup])

    const handleNewFollow = (actionVerb) => {
        apiProfileFollowToggle(username, actionVerb, (response, status)=>{
            // console.log(response, status)
            if (status===200) {
                setProfile(response)
                // apiProfileDetail(username, handleBackendLookup)
            }
            setProfileLoading(false)
        })
        setProfileLoading(true)
        
    }
    return didLookup === false ? "Loading..." : profile ? <ProfileBadge user={profile} didFollowToggle={handleNewFollow} profileLoading={profileLoading} /> : null
}