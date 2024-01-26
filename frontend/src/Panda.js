import { useState } from 'react';
import './Panda.css';
import Uploader from './components/uploader';

function Panda(){
    const [showUploader, setShowUploader] = useState(false);

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

    return (
        <div className="panda-container">
            <h1>Embedding</h1>
            <a className="panda-button" onClick={addFile}>Add a file</a>
           {showUploader? (<div className="panda-uploader">
                <button className="panda-close-btn" onClick={hideUpload}>X</button>
                <Uploader />
            </div>): null
            }
        </div>
    );
}

export default Panda;