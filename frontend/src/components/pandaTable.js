import './pandaTable.css';
import {updateEmbeddingRecord} from '../api/embedding';

function PandaTable(props) {
    const items = props.items;
    const getRecords= props.getRecords;
    // console.log(items);

    const deleteEmbedding =(item)=>{
        // TODO
        console.log('start to remove emb_id: '+item.emb_id);
        let params ={
            'embId': item.emb_id,
            'fileStatus': 'Deleted'
        };

        if(window.confirm('Are you sure you want to delete this record?')){
            updateEmbeddingRecord(params).then((response)=>{
                console.log('removed '+response.data);
                // request backend to remove datas in Vector databse
                // TODO
    
                // refresh list after remove is done
                getRecords();
            }).catch((error)=>{
                console.log('remove error: '+error);
            });
        }        
    }

    const chatWithLLM =() =>{
        // TODO redirect to chat page with LLM

    }

    return (
      <table className="panda-table">
        <thead>
            <tr>
                <th scope='col' id='fileName'>File Name</th>
                <th scope='col' id='owner' className='ten-cent'>Owner</th>
                <th scope='col' id='size' className='ten-cent'>Size</th>
                <th scope='col' id='status' className='ten-cent'>Status</th>
                <th scope='col' id='path' className='ten-cent'>Path</th>
                <th scope='col' id='fileDate' className='ten-cent'>Date</th>
            </tr>
        </thead>
        <tbody>
            {items.map((item) =>
            <tr key={item.emb_id}>
                <td className='table-first-col'>
                    <strong>{item.file_name}</strong>
                    <div className='table-col-ops'>
                       <span><a onClick={() => deleteEmbedding(item)}>Delete</a> | </span> 
                       <span> <a onClick={chatWithLLM}>Chat</a></span>
                    </div>    
                </td>
                <td className='table-col blue-color'>{item.owner}</td>
                <td className='table-col'>{item.file_size}K</td>
                <td className='table-col'>{item.file_status}</td>
                <td className='table-col'>-</td>
                <td className='table-col'>{item.file_datetime}</td>
            </tr>
            )}            
        </tbody>       
      </table>
    );
   }

export default PandaTable;