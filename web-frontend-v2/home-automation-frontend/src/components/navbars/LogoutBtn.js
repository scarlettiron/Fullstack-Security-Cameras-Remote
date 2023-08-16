import React, {useContext} from 'react'
import AuthContext from '../../context/AuthContext'
import '../../css/navbars.css'

const LogoutBtn = () => {
    const {logoutUser} = useContext(AuthContext)
  return (
    <div>
        <button onClick={logoutUser} className='nav-btn'>
            Logout
        </button>
    </div>
  )
}

export default LogoutBtn