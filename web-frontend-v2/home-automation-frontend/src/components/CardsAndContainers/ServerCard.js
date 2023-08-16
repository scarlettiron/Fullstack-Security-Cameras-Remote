import React, {useState, useContext} from 'react'
import DeviceContext from '../../context/DeviceContext'
import Button2 from '../buttonsAndInputs/Button2'
import { ReactComponent as ArrowUp } from '../../assets/up-chevron.svg'
import { ReactComponent as ArrowDown} from '../../assets/down-chevron.svg'
import ServerCardDropdown from './ServerCardDropdown'
import '../../css/cards-and-containers.css'

const ServerCard = ({title, type}) => {
    const [dropDown, setDropDown] = useState(false)
    const toggle = () => {
        setDropDown(!dropDown)
    }

    const {allDevices} = useContext(DeviceContext)
    console.log(allDevices)

  return (
    <div className='main-card'>
        <div className='padding-10 justify-content-between'>
            <div className='justify-content-end display-inline w-75'>
                <h1 className='text-white padding-0'>{title}</h1>
            </div>
                <Button2 
                action={toggle} 
                text={dropDown ? <ArrowUp className='svg1'/> : <ArrowDown className='svg1'/> } 
                wrapperClass = 'justify-content-center'
                />
        </div>

        {dropDown === true && (
            allDevices && allDevices.servers.length > 0 ?
                allDevices.servers.map((device, index) => {
                    return <ServerCardDropdown device={device} key={index}/>
                })
            :
                <ServerCardDropdown device={{name:`No ${title}`, id:null}} />
            )
        }
       
    </div>
  )
}

export default ServerCard