import React from 'react'
import {ReactComponent as Plus} from '../../assets/add.svg'
import '../../css/general.css'
const AddBtn = ({onClick, btnClass = null}) => {
  return (
    <div className='justify-content-center'>
        <button className={btnClass ? `${btnClass} plusBtn` : 'plusBtn'}
         onClick={onClick}>
            <Plus className='svg2' viewBox="0 0 32 32"/>
        </button>
    </div>
  )
}

export default AddBtn