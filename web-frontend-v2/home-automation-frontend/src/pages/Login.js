import React, {useContext} from 'react'
import AuthContext from '../context/AuthContext'
import { useHistory } from 'react-router-dom'
import Input from '../components/buttonsAndInputs/Input'
import Button3 from '../components/buttonsAndInputs/Button3'
import Button4 from '../components/buttonsAndInputs/Button4'
import '../css/login.css'
import '../css/general.css'

const Login = () => {
    const history = useHistory()
    const {loginUser} = useContext(AuthContext)
  return (
    <div className='login-wrapper'>
          <form onSubmit={loginUser} id='loginForm' className='login-container'>
              <div className='w-100 justify-content-center'>
                <h2 className='text-white'> Login </h2>
              </div>
              <Input id='username' placeholder='username' type='text'/>
              <Input id='password' placeholder='password' type='password' />
              <div className='w-100 justify-content-space-around margin-tb-20'>
                <Button3 text={'Signup'} action={() => {history.push('/signup')}}/>
                <Button4 text='Login' type='submit' form='loginForm'/>
              </div>
          </form>
    </div>
  )
}

export default Login