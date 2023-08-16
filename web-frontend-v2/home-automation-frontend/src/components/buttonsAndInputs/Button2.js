import React from 'react'
import '../../css/general.css'

//for dropdowns and svg buttons
const Button2 = ({text, action, wrapperClass=null}) => {
  return (
    <div className={wrapperClass}>
        <button className='button2' onClick={action}>{text}</button>
    </div>
  )
}

export default Button2