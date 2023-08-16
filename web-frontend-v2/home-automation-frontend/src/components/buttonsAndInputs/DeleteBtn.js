import React from 'react'
import '../../css/general.css'

const DeleteBtn = ({onClick, text=null}) => {
  return (
    <div className='justify-content-center'>
        <button className='deleteBtn' onClick={onClick}>
            {text ? text : 'Delete'}
        </button>
    </div>
  )
}

export default DeleteBtn