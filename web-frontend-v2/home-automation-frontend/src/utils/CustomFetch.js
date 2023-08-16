import dayjs from 'dayjs'
import GetCookie from './GetCookie'
import jwt_decode from 'jwt-decode'
import {loginRefreshUrl} from './ApiEndpoints'

const updateToken = async (AuthTokens) => {
    if(AuthTokens.refresh){
        const response = await fetch(loginRefreshUrl, {
            method:'POST',
            headers:{
                'Content-Type':'application/json',

            },
            body:JSON.stringify({'refresh':AuthTokens?.refresh})
        })
        let data = await response.json()
        localStorage.setItem('authTokens', JSON.stringify(data))
        return {response, data}
    }
    
}

const CustomFetch = async (dataUrl, fetchConfig={}, contentTypeOverRide=false) => {
    const AuthTokens = JSON.parse(localStorage.getItem('authTokens'))
    const User = jwt_decode(AuthTokens.access)
    let tokens = AuthTokens
    const expired = dayjs.unix(User.exp).diff(dayjs()) < 1

    if(expired){
        const {response, data} = await updateToken(AuthTokens)
        console.log(data)
        if(response.status === 200){
            tokens = await data
        }
        else{ 
            return {response, data}}
    }


    const csrfToken = GetCookie('csrftoken')
   
    if(!fetchConfig['headers']){
        fetchConfig['headers'] = {}
    }

    //add csrf token and authorization access token to passed in fetch configuration headers
    if(csrfToken){
    fetchConfig['headers']['X-CSRFToken'] = csrfToken
    }
    fetchConfig['headers']['Authorization'] = 'Bearer ' + tokens.access
    
    if(!fetchConfig['headers']['Content-Type'] && !contentTypeOverRide){
        fetchConfig['headers']['Content-Type'] =  'application/json'
    }

    console.log(fetchConfig)
    //continue with request
    const response = await fetch(dataUrl, fetchConfig)
    console.log(response)
    let data = {}
    if(response.status === 204){
        data = {'status':'deleted'}
    }
    else{
         data = await response.json()
    }


    // return fetch response
    return {response, data}
}

export default CustomFetch;