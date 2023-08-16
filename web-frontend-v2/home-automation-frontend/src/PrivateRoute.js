import React, {useContext} from 'react'
import AuthContext from './context/AuthContext'
import { Redirect, Route } from 'react-router-dom'

const PrivateRoute = ({children, ...rest}) => {
  const {AuthTokens} = useContext(AuthContext)
  return (
    <Route  {...rest}>
        {AuthTokens ? children : <Redirect to='/login'/>}
    </Route>
  )
}

export default PrivateRoute