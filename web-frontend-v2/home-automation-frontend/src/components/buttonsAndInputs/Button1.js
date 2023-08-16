import React from 'react'
import '../../css/general.css'


//for forms solid theme secondary with white text
const Button1 = ({text, onclick = null, type=null, form=null}) => {
  return (
    <div>
        <button className='button1' onClick={onclick} type={type} form={form}>
          {text}
        </button>
    </div>
  )
}

export default Button1