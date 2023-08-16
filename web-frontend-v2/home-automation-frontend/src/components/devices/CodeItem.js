import React, {useState, useContext} from 'react'
import DeviceContext from '../../context/DeviceContext'
import DeleteBtn from '../buttonsAndInputs/DeleteBtn'
import CustomFetch from '../../utils/CustomFetch'
import { devicePw } from '../../utils/ApiEndpoints'
import '../../css/general.css'
import '../../css/edit-add-device.css'

const CodeItem = ({code}) => {
    const {pwDetail} = devicePw
    const [loading, setLoading] = useState()
    const {removeDeviceCode} = useContext(DeviceContext)

    const deleteCode = async () =>{
        console.log(code)
        setLoading(true)
        const fetchConfig = {method:'DELETE'}
        const {response, data} = await CustomFetch(`${pwDetail.url}${code.id}/`, fetchConfig)
        if(response.status === 204){
            removeDeviceCode(code.device, code.id)
        }
        setLoading(false)
    }

  return (
    <div className='code-container'>
        <div className='w-75'>
            <h3 className='text-white'>{code.code}</h3>
        </div>
        <DeleteBtn onClick={deleteCode}/>
    </div>
  )
}

export default CodeItem