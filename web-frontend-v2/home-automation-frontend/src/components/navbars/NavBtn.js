import React from 'react'
import { useHistory } from 'react-router-dom'
import '../../css/navbars.css'

const NavBtn = ({route, text}) => {
  const history = useHistory()

  const linkTo = () => {
    history.push(`/${route}`)
  }
  
  return (
    <div>
        <button onClick={linkTo} className='nav-btn'>
            {text}
        </button>
    </div>
  )
}

export default NavBtn