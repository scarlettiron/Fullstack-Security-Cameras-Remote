import React from 'react'
import '../../css/general.css'

const ExitBtn = ({action = null, wrapperClass=null}) => {
  
  return (
    <div className='justify-content-center'>
        <button className='exitBtn' onClick={action}>X</button>
    </div>
  )
}

export default ExitBtn