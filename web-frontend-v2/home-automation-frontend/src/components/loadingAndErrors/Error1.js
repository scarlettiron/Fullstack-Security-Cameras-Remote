import React from 'react'
import '../../css/errors-and-success.css'

const Error1 = ({message = null, wrapperClass=null}) => {
  return (
    <div className={wrapperClass ? wrapperClass : 'w-100'}>
      <div className='error-container margin-0'>
          <h5 className='text-white margin-0'>Error: {message ? message : 'try again later'}</h5>
      </div>
    </div>
  )
}

export default Error1