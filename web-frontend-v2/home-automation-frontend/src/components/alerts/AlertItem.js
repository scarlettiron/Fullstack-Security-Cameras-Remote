import React, {useState} from 'react'
import { convertToFormattedSiteDate, convertToFormattedSiteTime} from '../../utils/DateFunctions'
import {ReactComponent as ArrowDown} from '../../assets/down-chevron.svg'
import {ReactComponent as ArrowUp} from '../../assets/up-chevron.svg'
import Button2 from '../buttonsAndInputs/Button2'
import '../../css/general.css'
import '../../css/cards-and-containers.css'


export const AlertItem = ({alert}) => {
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
                        <h4 className='text-white margin-0'>{alert.type} at {alert.device.name}</h4>
                    </div>
                    <div className='w-100'>
                        <h6 className='text-secondary padding-0 margin-0'>{convertToFormattedSiteDate(alert.date)}  {convertToFormattedSiteTime(alert.date)}</h6>
                    </div>
                </div>
                <Button2 
                action={toggle} 
                text={dropDown ? <ArrowUp className='svg1'/> : <ArrowDown className='svg1'/> } 
                wrapperClass = 'justify-content-center'
                />
            </div>

            {dropDown &&

            <div className='alert-dropdown w-100 padding-10'>
                {
                    alert.type === 'intruder' ? 
                    <>
                        <div className='alert-image-container'>
                            {alert.imager ?
                                <img className='alert-image' src={alert.image} alt={alert.type}/>
                                :
                                <h5 className='text-white'>No Image Available</h5>
                            }               
                        </div>
                    </>
                    :
                    <>
                        <div className='w-100 justify-content-center padding-5'>
                            <h5 className='text-secondary'>{alert.description ? alert.description : "No description"}</h5>
                        </div>
                    </>
                }
            </div>
            }

        </div>
    </div>
    )
}

export default AlertItem
