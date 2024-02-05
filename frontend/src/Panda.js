import { useEffect, useState } from 'react';
import './Panda.css';
import Uploader from './components/uploader';
import PandaTable from './components/pandaTable';
import {getEmbeddingRecords} from './api/embedding';

function Panda(){
    const [showUploader, setShowUploader] = useState(false);
    const [items, setItems] = useState([]);
    const addFile =()=>{
        if(!showUploader){
            setShowUploader(true);
        }
    }

    const hideUpload =()=>{
        if(showUploader){
            setShowUploader(false);
        }
    }

    useEffect(()=>{
        getRecords();
    }, []);

    // get list of embedding record
    async function getRecords(){
        // alert("I am your farther's method, son!!!");
        getEmbeddingRecords().then((response)=>{
            // console.log(response.data);
            setItems(response.data);
        }).catch((error)=>{
            console.log(error);
        });
    }

    return (
        <div className="panda-container">
            <h1>Embedding</h1>
            <a className="panda-button" onClick={addFile}>Add a file</a>
           {showUploader? (<div className="panda-uploader">
                <button className="panda-close-btn" onClick={hideUpload}>X</button>
                <Uploader getRecords={getRecords}/>
            </div>): null
            }
            <div className='panda-list'>
                <PandaTable items={items} getRecords={getRecords}/>
            </div>
        </div>
    );
}

export default Panda;