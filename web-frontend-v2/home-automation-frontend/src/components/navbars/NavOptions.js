import React, {useContext} from 'react'
import AuthContext from '../../context/AuthContext'
import NavBtn from './NavBtn'
import LogoutBtn from './LogoutBtn'
import '../../css/navbars.css'
import '../../css/general.css'
import { userUrls } from '../../utils/ApiEndpoints'

const NavOptions = ({flag}) => {
  const {logoutUser, User} = useContext(AuthContext)
  return (
    <div className={`${flag} side-nav-wrapper`}>
          <NavBtn
          text='Home'
          route='home'
          />

          <NavBtn
          text='Alerts'
          route='alerts'
          />

          <NavBtn
          text='Add Device' 
          route='add-device'
          />

          <NavBtn
          text='Add Home Server' 
          route='add-server'
          />
          
          <NavBtn
          text='Edit Household'
          route='edithousehold'
          />

          <NavBtn
          text='Get Started'
          route='/get-started'
          />

          <LogoutBtn/>
    </div>
  )
}

export default NavOptions