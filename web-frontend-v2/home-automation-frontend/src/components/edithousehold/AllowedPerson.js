import React, {useState, useCallback, useContext} from 'react'
import SocketContext from '../../context/SocketContext'
import CustomFetch from '../../utils/CustomFetch'
import { allowed_persons } from '../../utils/ApiEndpoints'
import {ReactComponent as ArrowDown} from '../../assets/down-chevron.svg'
import {ReactComponent as ArrowUp} from '../../assets/up-chevron.svg'
import Button2 from '../buttonsAndInputs/Button2'
import Button3 from '../buttonsAndInputs/Button3'
import DeleteBtn from '../buttonsAndInputs/DeleteBtn'
import Error1 from '../loadingAndErrors/Error1'
import LoadingSpinner1 from '../loadingAndErrors/LoadingSpinner1'
import { CountRenders } from '../../utils/CountRenders'
import EditPersonPopup from './EditPersonPopup'
import '../../css/general.css'


const AllowedPerson = ({person, handleRemovePerson, handleSetPerson}) => {
    CountRenders('allowed person: ')
    const {handleUpdateHomeServerPersons} = useContext(SocketContext)
    const {getAllowedPersonDetail} = allowed_persons
    const [dropDown, setDropDown] = useState(() => false)
    const [editPopup, setEditPopup] = useState(() => false)
    const [p, setP] = useState(person)
    
    const toggle = () => {
        setDropDown(() => !dropDown)
    }

    const [loading, setLoading] = useState(() => false)
    const [error, setError] = useState(() => null)

    const handleSetP = (data) => {
        setP(data)
    }

    const handleDeletePerson = useCallback(async () => {
        setError(() => null)
        setLoading(() => true)
        const fetchConfig = {method:'DELETE'}
        const {response, data} = await CustomFetch(`${getAllowedPersonDetail.url}${person.id}/`, fetchConfig)
        if(response.status === 204){
            handleRemovePerson(person.id)
            await handleUpdateHomeServerPersons()
            setLoading(() => false)
            return
        }
        setError(() => 'Unable to process your request at this time, try again later')
    }, [person, handleSetPerson, handleRemovePerson])

    console.log(editPopup)

    const handleSetPopup = () => {
        console.log('clicked')
        setEditPopup(!editPopup)
    }

  return (
        <div className='allowed-person-container'>
            <div className='justify-content-end display-inline w-75'>
            <h3 className='text-white'>{p.name}</h3>
            </div>

            <div className='display-inline'>
                <Button2 
                action={toggle} 
                text={dropDown ? <ArrowUp className='svg1'/> : <ArrowDown className='svg1'/> } 
                wrapperClass = 'justify-content-center'
                />
            </div>

            {dropDown &&
                <>
                    {error &&
                        <div className='w-75'>
                            <Error1 message={error}/>
                        </div>
                    }
                    {editPopup &&
                        <EditPersonPopup 
                        person={p}
                        handleSetPerson = {handleSetPerson}
                        closePopup = {handleSetPopup}
                        handleSetP = {handleSetP}
                        />
                    }
                    <div className='w-100 padding-10 justify-content-space-around'>
                        <DeleteBtn onClick={loading ? null : handleDeletePerson} text={loading ? <LoadingSpinner1/> : null}/>
                        <Button3 text={'Edit'} action={handleSetPopup}/>
                    </div>
                    <div className='w-100'>
                            <img className='allowed-person-image' alt={p.name} src={p.pic}/>
                    </div>
                </>
            }


        </div>
  )
}

export default React.memo(AllowedPerson)