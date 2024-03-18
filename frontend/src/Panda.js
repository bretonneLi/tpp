import { useEffect, useState } from 'react';
import './Panda.css';
import Uploader from './components/uploader';
import PandaTable from './components/pandaTable';
import {getEmbeddingRecords, addLLMSetting, getCurrentLLM, queryLlmList} from './api/embedding';

function Panda(){
    const [showUploader, setShowUploader] = useState(false);
    const [items, setItems] = useState([]);
    const [currentLLM, setCurrentLLM] = useState('');
    const [showLLM, setShowLLM] = useState(false);
    const [llmList, setLlmList] = useState([]);

    const addFile =()=>{
        if(!showUploader){
            setShowUploader(true);
        }
    }

    const setLLM =()=>{
        setShowLLM(!showLLM);
    }

    const hideUpload =()=>{
        if(showUploader){
            setShowUploader(false);
        }
    }

    const handleModelChange = (event) => {
        if(currentLLM!= event.target.value){
            if(window.confirm('Are you sure to change the current LLM?')==true){
                setCurrentLLM(event.target.value);
                addLLMSetting({'llmName': event.target.value}).then((response)=>{                    
                                         
                }).catch((error)=>{
                    console.log(error);
                });                
            }
        }       
    };

    useEffect(()=>{
        getRecords();
        getLlmList();        
    }, []);

    // get list of embedding record
    async function getRecords(){
        getEmbeddingRecords().then((response)=>{
            // console.log(response.data);
            setItems(response.data);
        }).catch((error)=>{
            console.log(error);
        });
    }

    // get list of embedding record
    async function getLlmList(){
        queryLlmList().then((response)=>{
            // console.log(response.data);
            setLlmList(response.data);
            getLLM();
        }).catch((error)=>{
            console.log(error);
        });
    }

    async function getLLM(){
        getCurrentLLM().then((response)=>{
            // console.log(response);
            setCurrentLLM(response.data.llm_name);
        }).catch((error)=>{
            console.log(error);
        });
    }

    return (
        <div className="panda-container">
            <div className='panda-adding'>
                <h1>Embedding</h1>
                <a className="panda-button" onClick={addFile} title="add a file"><span className="dashicons dashicons-plus-alt"></span>Add a file</a>
                <div className='panda-setting'>
                    Current LLM: <span className='panda-llm'>{currentLLM}</span>
                    <a className="panda-button" onClick={setLLM} title=""><span className="dashicons dashicons-admin-generic"></span>Setting</a>
                   {showLLM?( <select value={currentLLM} onChange={handleModelChange}>
                        {llmList.map((llm)=>(
                            <option key={llm} value={llm}>{llm}</option>
                        ))}
                    </select>):null}
                </div>                
            </div>
           {showUploader? (<div className="panda-uploader">
                <button className="panda-close-btn" onClick={hideUpload}>X</button>
                <Uploader getRecords={getRecords} llm={currentLLM}/>
            </div>): null
            }
            <div className='panda-list'>
                <PandaTable items={items} getRecords={getRecords}/>
            </div>
        </div>
    );
}

export default Panda;