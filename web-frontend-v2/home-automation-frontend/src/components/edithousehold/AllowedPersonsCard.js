import React, {useState} from 'react'
import {ReactComponent as ArrowDown} from '../../assets/down-chevron.svg'
import {ReactComponent as ArrowUp} from '../../assets/up-chevron.svg'
import Button2 from '../buttonsAndInputs/Button2'
import '../../css/general.css'
import AllowedPersonCardDropdown from './AllowedPersonCardDropdown'

const AllowedPersonsCard = () => {
    const [dropDown, setDropDown] = useState(false)
    const toggle = () => {
        setDropDown(!dropDown)
    }


  return (
    <div className='w-100 justify-content-center flex-wrap margin-10'>
        <div className='alert-card'>
            <div className='padding-10 justify-content-between'>
                <div className='display-inline w-75 margin-5'>
                    <div className='flex-wrap w-100'>
                        <h3 className='text-white'>Allowed People</h3>
                    </div>
                </div>
                <Button2 
                action={toggle} 
                text={dropDown ? <ArrowUp className='svg1'/> : <ArrowDown className='svg1'/> } 
                wrapperClass = 'justify-content-center'
                />
            </div>
            {dropDown &&
            <AllowedPersonCardDropdown/>
            }
        </div>
    </div>
  )
}

export default AllowedPersonsCard