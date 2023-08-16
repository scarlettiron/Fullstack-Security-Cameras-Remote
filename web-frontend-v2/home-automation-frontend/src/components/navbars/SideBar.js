import React, {useState} from 'react'
import {ReactComponent as Gear} from '../../assets/gear.svg'
import NavOptions from './NavOptions'
import '../../css/navbars.css'
import '../../css/general.css'


const SideBar = () => {
  const [toggle, setToggle] = useState(() => false)

  const handleToggle = () => {
    console.log('toggled')
    setToggle(!toggle)
  }

  return (
    <div className='side-nav-container'>
        <button className={toggle ? 'nav-btn toggle-btn-active' : 'nav-btn toggle-btn'} onClick={handleToggle}>
          <Gear className='svg1' viewBox="0 0 512.000000 512.000000"/>
        </button>
      
      {/* dropdown for tablets and mobile devices*/ }
      <NavOptions flag={toggle ? 'mobile active' : 'mobile'}/>
      {/*options for desktop and larger screens*/}
      <NavOptions flag={'desktop'}/>
    </div>

      
  )
}

export default SideBar