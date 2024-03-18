import React,{useMemo, useState} from 'react';
import {useDropzone} from 'react-dropzone';
import './uploader.css';
import '../Panda.css';
import {uploadFile,addEmbeddingRecord,updateEmbeddingRecord} from '../api/embedding'

function Uploader(props) {
  const {getRecords, llm} = props;
  const [resMsg, setResMsg] = useState('uploaded OK.');
    const baseStyle = {
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: '20px',
        borderWidth: 2,
        borderRadius: 2,
        borderColor: '#eeeeee',
        borderStyle: 'dashed',
        backgroundColor: '#fafafa',
        color: '#bdbdbd',
        outline: 'none',
        transition: 'border .24s ease-in-out'
      };
      
      const focusedStyle = {
        borderColor: '#2196f3'
      };
      
      const acceptStyle = {
        borderColor: '#00e676'
      };
      
      const rejectStyle = {
        borderColor: '#ff1744'
      };

    const updateEmbedding=(params)=>{
      // update file status and vector ids
      updateEmbeddingRecord(params).then((response)=>{
        // console.log("updated "+response.data);
         // refresh table list
        getRecords();
      }).catch((error)=>{
        console.log("updated eror : "+error);
      });
    }
      
    const uploadEmbedding = (file, embId) => {
      let request = uploadFile("embedding/pdf_retriever/", file, embId, llm);
      request.then((response)=>{
        // file sent successfully
        console.log(response.status);
        console.log(response.data);
        if(response){
          // get embedding response ok
          let params = {
            'embId': embId,
            'fileStatus': 'Uploaded',
            'vectorIds': JSON.stringify(response.data)
          };
          // update file status and vector ids
          updateEmbedding(params);
        }       
      }).catch((error)=>{
        console.log('file sent failed .', error);
        setResMsg('File uploading failed.');
      });
    };

    // send uploaded file to server side with requesting web api
    const onDrop = (acceptedFiles)=>{
      console.log('start...')
      let uploadedFile = acceptedFiles[0];
      let params = {
        'fileName': uploadedFile.path,
        'fileSize': (uploadedFile.size / 1000).toFixed(1),
      }
      // start to save data to wp data table
      addEmbeddingRecord(params).then((response)=>{
        // console.log(response);
        if(response.data>0){
          // get right embedding file id, then send file to backend for embedding processing
          uploadEmbedding(uploadedFile, response.data);
        }else{
          setResMsg('File record save failed.');
        }
      }).catch((error)=>{
        setResMsg('File record save failed.');
        console.log('embedding record save failed');
      })
    };

    const {
      open,
      acceptedFiles, 
      getRootProps, 
      getInputProps, 
      isFocused,
      isDragAccept,
      isDragReject} = useDropzone({
        accept:{
          'application/pdf': ['.pdf'], 
        },
        maxSize: 134217728, // 128Mb
        multiple: false,
        onDrop,
      });
    
    const style = useMemo(() => ({
      ...baseStyle,
      ...(isFocused ? focusedStyle : {}),
      ...(isDragAccept ? acceptStyle : {}),
      ...(isDragReject ? rejectStyle : {})
    }), [
      isFocused,
      isDragAccept,
      isDragReject
    ]);

    const files = acceptedFiles.map(file => (
      <li key={file.path}>
        {file.path} - {file.size} bytes -- {resMsg?(<em>{resMsg}</em>):null}
      </li>
    ));

    return (
      <section className="container">
        <div {...getRootProps({style})}>
          <input {...getInputProps()} />
          <p className="up-bold-text">Upload your file to LLM</p>
          <p className="up-text">Click the area or drop your file to area.</p>
          <p className="up-text">Only *.pdf will be accepted</p>
          <p className="up-text">Size limit up to: 128MB.</p>
        </div>
        <aside>
          <h4>Files</h4>
          <ul>{files}</ul>
        </aside>
      </section>
    );
  }

export default Uploader;