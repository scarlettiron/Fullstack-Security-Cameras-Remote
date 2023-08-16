import React from 'react'
import '../../css/general.css'


//for actions and links, solid theme tertiary with white text
const Button3 = ({action, text}) => {
  return (
    <div>
        <button onClick={action} className='button3'>
            {text}
        </button>
    </div>
  )
}

export default Button3