import './pandaTable.css';

function PandaTable(props) {
    const{items} = props;
    // console.log(items);

    const deleteEmbedding =() =>{
        // TODO

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
                       <span><a onClick={deleteEmbedding}>Delete</a> | </span> 
                       <span> <a onClick={deleteEmbedding}>Talk</a></span>
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