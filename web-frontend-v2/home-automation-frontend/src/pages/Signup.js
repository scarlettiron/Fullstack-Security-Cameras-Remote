import React, {useState, useContext} from 'react'
import { useHistory } from 'react-router-dom'
import AuthContext from '../context/AuthContext'
import CustomFetch from '../utils/CustomFetch'
import Error1 from '../components/loadingAndErrors/Error1'
import LoadingSpinner1 from '../components/loadingAndErrors/LoadingSpinner1'
import {userUrls} from '../utils/ApiEndpoints'
import Input from '../components/buttonsAndInputs/Input'
import Button3 from '../components/buttonsAndInputs/Button3'
import Button4 from '../components/buttonsAndInputs/Button4'
import '../css/login.css'
import '../css/general.css'

const Signup = () => {
    const history = useHistory()

    const {createUser} = userUrls
    const [error, setError] = useState(null)
    const [loading, setLoading] = useState(false)

    const {loginUser} = useContext(AuthContext)

    const handleCreateUser = async (e) => {
        e.preventDefault()
        setError(null)

        const email = e.target.email.value
        const username = e.target.username.value
        const password = e.target.password.value
        const verify_password = e.target.verifypassword.value 
    
        console.log(email)
        console.log(username)
        console.log(password)

        if(password !== verify_password){
            setError('Passwords do not match')
            return
        }

        if(!email || !username || !password){
            setError("Fill out all fields")
            return
        }

        setLoading(true)
        
        const fetchConfig = {
            method : 'POST',
            body : JSON.stringify({
                email:email,
                username:username,
                password:password
            }),
            headers:{
                'Content-Type':'application/json',
            },
        }
        const response = await fetch(createUser.url, fetchConfig)
        const data = await response.json()
        console.log(data)

        if(response.status === 201){
            loginUser(e)
            return
        }
        else{
            setError(data)
            setLoading(false)
        }

    }

    return (
        <div className='login-wrapper'>
              <form onSubmit={handleCreateUser} id='signupForm' className='login-container'>
                  <div className='w-100 justify-content-center'>
                    <h2 className='text-white'> Signup  </h2>
                  </div>
                  <div className='w-100 justify-content-center'>
                    {error &&
                        <Error1 message={error}/>
                    }
                  </div>
                  <Input id='email' placeholder='email' type='email'/>
                  <Input id='username' placeholder='username' type='text'/>
                  <Input id='password' placeholder='password' type='password' />
                  <Input id='verifypassword' placeholder='re-enter password' type='password' />
                  <div className='w-100 justify-content-space-around'>
                    <Button3 text={"Login"} action={() => {history.push('/login')}}/>
                    <Button4 text={loading ? <LoadingSpinner1 size='lds-btn-size'/> : 'Signup'} type='submit' form={loading ? null : 'signupForm'}/>
                  </div>
              </form>
        </div>
      )
}

export default Signup