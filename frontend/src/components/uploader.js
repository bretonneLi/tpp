import React,{useMemo} from 'react';
import {useDropzone} from 'react-dropzone';
import './uploader.css';
import '../Panda.css';
import {uploadFile} from '../api/embedding'
function Uploader(props) {
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

    // send uploaded file to server side with requesting web api
    const onDrop = (acceptedFiles)=>{
      console.log('start...')
      let request = uploadFile("/mockuploadfile/", acceptedFiles[0]);
      request.then((response)=>{
        // file sent successfully
        console.log(response.status);
        console.log(response.data);
      }).catch((error)=>{
        console.log('file sent failed .', error);
      });
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
        {file.path} - {file.size} bytes
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