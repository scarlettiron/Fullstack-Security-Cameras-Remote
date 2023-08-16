import React from 'react'
import '../../css/general.css'

//secondary style button, primary theme with theme secondary outline
const Button4 = ({text, action, form=null, type=null}) => {
  return (
    <div>
      {form ?         
            <button onClick={action} className='button4' form={form} type={type}>
              {text}
            </button>
            :

            <button onClick={action} className='button4'>
              {text}
            </button>
      }
    </div>
  )
}

export default Button4