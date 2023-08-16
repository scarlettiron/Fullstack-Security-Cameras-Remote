import React, {createContext, useState, useEffect, useCallback} from "react";
import jwt_decode from 'jwt-decode'
import { loginUrl, loginRefreshUrl} from "../utils/ApiEndpoints";
import { useHistory } from "react-router-dom";
import GetCookie from "../utils/GetCookie";
import { CountRenders } from "../utils/CountRenders";
import dayjs from 'dayjs'

const AuthContext = createContext()

export default AuthContext;

export const AuthProvider = React.memo(({children}) => {
    CountRenders('auth context')

    const [AuthTokens, setAuthTokens] = useState(() => localStorage.getItem('authTokens') ? JSON.parse((localStorage.getItem('authTokens'))) :  null)
    const [User, setUser] = useState(() => localStorage.getItem('authTokens') ? jwt_decode(JSON.parse(localStorage.getItem('authTokens'))?.access) : null)
    const [loading, setLoading] = useState(() => true)
    const history = useHistory()

    const loginUser = useCallback(async (e) => {
        e.preventDefault()
        const payload = {
            'username':e.target.username.value,
            'password':e.target.password.value
        }

        const response = await fetch(loginUrl, {
            method:'POST',
            headers: {
                'Content-Type':'application/json'
            }, 
            body:JSON.stringify(payload)
        })
        if (response.status === 200){
            const data = await response.json()
            const user = jwt_decode(data.access)
            setAuthTokens(() => data)
            setUser(() => user)
            localStorage.setItem('authTokens', JSON.stringify(data))
            localStorage.setItem('user', JSON.stringify(user))
            history.push('/home')
            }
        else{history.push('/')} 
    }, [setAuthTokens])

    const logoutUser = useCallback(() => {
        console.log("logging out user")
        localStorage.removeItem('authTokens')
        setAuthTokens(null)
        localStorage.removeItem('user')
        setUser(null)
        history.push('/login')
    },[setAuthTokens])




    
    const updateToken = useCallback(async () => {
        const csrf = GetCookie('csrftoken')
        const refresh = AuthTokens?.refresh
        if(refresh){
            const response = await fetch(loginRefreshUrl, {
                method:"POST",
                headers:{
                    'Content-Type':'application/json',
                    'Authorization':csrf,
                },
                body:JSON.stringify({'refresh': refresh})
            })

            if(response.status === 200){
                const data = await response.json()
                if (data.refresh){
                    localStorage.setItem('authTokens', JSON.stringify(data))
                    setAuthTokens(() => data)
                    const user = jwt_decode(data.access)
                    setUser(() => user)

                    if(loading){
                        setLoading(false)
                    }
                    return {response, data}
                }
            }
            else{
                logoutUser()
            }
        }

    },[AuthTokens, setUser])

    const contextData = {
        loginUser:loginUser,
        logoutUser:logoutUser,
        User:User,
        setUser : setUser,
        AuthTokens:AuthTokens,
        setAuthTokens:setAuthTokens,
        updateToken:updateToken,
    }

     useEffect(() => {
         
        const updateData = async () => { await updateToken();}
        if(loading){
            if(!AuthTokens) return
            const User = jwt_decode(AuthTokens.access)
            const expired = dayjs.unix(User.exp).diff(dayjs()) < 1
            if(!expired) return 
            updateData()
        }

        const interval = setInterval(()=>{
            if(AuthTokens){
                updateData()
            }
        })
        return ()=> clearInterval(interval)
    }, [AuthTokens, loading])
    

    return (
        <AuthContext.Provider value={contextData}>
            {children}
        </AuthContext.Provider>
    )
})