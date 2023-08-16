import React, {useState, useContext} from 'react'
import SocketContext from '../../context/SocketContext'
import Input from '../../components/buttonsAndInputs/Input'
import Button3 from  '../../components/buttonsAndInputs/Button3'
import Button4 from  '../../components/buttonsAndInputs/Button4'
import FileInput from '../../components/buttonsAndInputs/FileInput'
import LoadingSpinner1 from '../../components/loadingAndErrors/LoadingSpinner1'
import CustomFetch from '../../utils/CustomFetch'
import { allowed_persons } from '../../utils/ApiEndpoints'
import Error1 from '../../components/loadingAndErrors/Error1'
import Success1 from '../../components/loadingAndErrors/Success1'
import ExitBtn from '../buttonsAndInputs/ExitBtn'
import '../../css/popups.css'
import '../../css/general.css'

const EditPersonPopup = ({person, closePopup, handleSetPerson, handleSetP}) => {
    const {handleUpdateHomeServerPersons} = useContext(SocketContext)
    const {getAllowedPersonDetail} = allowed_persons
    const [loading, setLoading] = useState(() => false)
    const [error, setError] = useState(() => null)
    const [success, setSuccess] = useState(() => null)
    const [thumbnail, setThumbnail] = useState(() => null)
    const [name, setName] = useState(() => person.name)

    const controller = new AbortController()
    const signal = controller.signal

    const handleAbort = () => {
        controller.abort()
        setLoading(false)
    }

    const handleSetName = (e) => {
        setName(() => e.target.value)
    }

    const handleUpdatePicState = (e) => {

        const file = e.target.files[0]
        const filePath = URL.createObjectURL(file)

        const newState = {
            'file':file,
            'path':filePath, 
        }

        setThumbnail(()=>newState)
    }

    const handleEditPerson = async (e) => {
        e.preventDefault()
        setError(null)
        setLoading(true)

        if(!thumbnail && !name){
            setError('Please provide valid name or photo')
            return
        } 

        const payload = new FormData()

        if(name){
            payload.append('name', name)
        }

        if(thumbnail && thumbnail.file){
            payload.append('pic', thumbnail.file)
        }

        const fetchConfig = {method:'PUT', body:payload, signal:signal}
        const {response, data} = await CustomFetch(`${getAllowedPersonDetail.url}${person.id}/`, fetchConfig, true)

        
        if(response.status === 200){
            await handleUpdateHomeServerPersons()
            setLoading(false)
            setSuccess(true)
            handleSetPerson(data)
            handleSetP(data)
            closePopup()
        }
        else{
            setError('error updating user')
            setLoading(false)
        }
    }
  return (
    <div className='w-100 justify-content-center'>
        {success &&
                <Success1/>
            }
            
            <div className='popup-container'>
                    <div className='w-100 justify-content-end padding-10'>
                        <ExitBtn action={closePopup} />
                    </div>

                    <h3 className='text-white'>Edit {person.name}</h3>
                    <div className='w-100 justify-content-center'>
                        <p className='text-white'>People added to your households
                            "Allowed People List" will not trigger alerts by facial recognition used
                            by camera's. (Photograph of person required)
                        </p>
                    </div>
                    {error &&
                        <Error1 message={error} wrapperClass={'w-75 justify-content-center'}/>
                    }
                    <div className='w-75'>
                        <Input 
                        id='name'
                        placeholder={person.name}
                        onChange={handleSetName}
                        />
                    </div>
                    <div className='w-75 justify-content-center flex-wrap padding-10'>
                        <div className='w-100'>
                            <FileInput 
                            id={'pic'} 
                            onChange={handleUpdatePicState}
                            />
                        </div>
                        <p className='text-white'>Person must be facing camera straight forward.</p>
                    </div>
                    {thumbnail && thumbnail.path &&
                        <img alt='new person' src={thumbnail.path} className='allowed-person-image'/>
                    }
                    <div className='justify-content-between w-75 padding-10 margin-10'>
                        <Button3 text='Cancel' action={loading ? handleAbort : closePopup} />
                        <Button4 text={loading ? <LoadingSpinner1 size='lds-btn-size' /> : 'Save'}
                        action = {loading ? ()=> {console.log('Cannot resubmit')} : handleEditPerson}
                        />
                    </div>
                </div>
            </div>
  )
}

export default EditPersonPopup