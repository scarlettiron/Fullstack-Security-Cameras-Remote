import React from 'react'
import '../../css/general.css'

const Input = ({id, placeholder, type='text', onChange=null, value=null, min=null, max=null}) => {
  return (
    <div className='margin-10'>
      {value ? 
        <input type={type} className={'input1'} placeholder={placeholder} 
        id={id} onChange={onChange} value = {value}/>
        :
        <input type={type} className={'input1'} placeholder={placeholder} 
        id={id} onChange={onChange} min={min} max={max}/>
    }
    </div>
  )
}

export default Input