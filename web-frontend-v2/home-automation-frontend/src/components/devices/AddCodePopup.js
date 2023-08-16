import React, {useState, useContext} from 'react'
import DeviceContext from '../../context/DeviceContext'
import CustomFetch from '../../utils/CustomFetch'
import { devicePw } from '../../utils/ApiEndpoints'
import Input from '../../components/buttonsAndInputs/Input'
import Button3 from  '../../components/buttonsAndInputs/Button3'
import Button4 from  '../../components/buttonsAndInputs/Button4'
import LoadingSpinner1 from '../../components/loadingAndErrors/LoadingSpinner1'
import Error1 from '../../components/loadingAndErrors/Error1'
import Success1 from '../../components/loadingAndErrors/Success1'
import ExitBtn from '../buttonsAndInputs/ExitBtn'
import '../../css/popups.css'
import '../../css/general.css'

const AddCodePopup = ({device, closePopup, updateDeviceCodes}) => {
    const {pwCreate} = devicePw

    const [loading, setLoading] = useState(() => false)
    const [error, setError] = useState(() => null)
    const [success, setSuccess] = useState(() => null)

    const {addDeviceCode} = useContext(DeviceContext)

    const controller = new AbortController()
    const signal = controller.signal

    const handleAbort = () => {
        controller.abort()
        setLoading(false)
    }

    const handleCreatePw = async (e) => {
        e.preventDefault()
        setError(null)

        const code = e.target.code.value
        if(!code){
            setError('Code required')
            setLoading(false)
            return
        }

        if(code.toString().length !== 4){
            setError('Code must be 4 digits long')
            setLoading(false)
            return
        }

        setLoading(true)

        const fetchConfig = {method:'POST', body:JSON.stringify({code:code, device:device.id})}
        console.log(fetchConfig)
        const {response, data} = await CustomFetch(pwCreate.url, fetchConfig)
        if(response.status === 201){
            addDeviceCode(data)
            updateDeviceCodes(data)
            setLoading(false)
            closePopup()
            return
        }
        setError('Could not create new code')
        setLoading(false)
    }


  return (
    <div className='w-100 justify-content-center'>
        {success &&
            <Success1/>
        }
            
        <div className='popup-container'>
            <div className='w-100 justify-content-end'>
                <ExitBtn action={closePopup} />
            </div>

            <h3 className='text-white margin-0 padding-0'>Create Passcode For Device</h3>
            <div className='w-100 justify-content-center margin-0 padding-0'>
                <p className='text-white margin-0 padding-0'>Add a passcode to the device, anyone with this
                code can unlock this deadbolt.
                </p>
            </div>
            {error &&
                <Error1 message={error} wrapperClass={'w-75 justify-content-center'}/>
            }
            <form className='w-100 justify-content-center' method='POST' onSubmit={handleCreatePw} id='addCodeForm'>
                <div className='w-75'>
                    <Input 
                    id='code'
                    placeholder='Code must be a 4 digit number'
                    type={'number'}
                    />
                </div>
            </form>
            <div className='justify-content-between w-75 padding-10 margin-10'>
                <Button3 
                text='Cancel' 
                action={loading ? handleAbort : closePopup} 
                />
                <Button4 
                text={loading ? <LoadingSpinner1 size='lds-btn-size' /> : 'Save'}
                form = {loading ? null : 'addCodeForm'}
                />
            </div>
            
        </div>
    </div>

  )
}

export default AddCodePopup