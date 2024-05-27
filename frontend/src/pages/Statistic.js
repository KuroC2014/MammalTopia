import { useEffect, useState } from "react";
import { Select, Space, Table, message } from 'antd';
import { postStatistic } from "../requests/api";
import { extractKeys } from "../utils/CommonUtils";

const options = [
    {
      label: 'Top Mammal Order Name By Continents',
      value: 1,
    },
    {
      label: 'Top Institutions By Extinct Mammals Recorded',
      value: 2,
    },
    {
      label: 'Top Favorited Mammals By Institutions',
      value: 3,
    },
    {
      label: 'Top Cited Mammal Institutions',
      value: 4,
    },
];

const mockData = [
    {
      key: '1',
      name: 'John Brown',
      age: 32,
      address: 'New York No. 1 Lake Park',
      tags: ['nice', 'developer'],
    },
    {
      key: '2',
      name: 'Jim Green',
      age: 42,
      address: 'London No. 1 Lake Park',
      tags: ['loser'],
    },
    {
      key: '3',
      name: 'Joe Black',
      age: 32,
      address: 'Sydney No. 1 Lake Park',
      tags: ['cool', 'teacher'],
    },
];

function Statistic() {

    const [dataList, setDataList] = useState([]);
    const [columns, setColumns] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [dataCount, setDataCount] = useState(0);
    const [selectedKey, setSelectedKey] = useState(1);


    useEffect(() => {
        postStatistic({
            statisticKey: selectedKey,
            page: currentPage
        }).then((data) => {
            let _dataList = data.dataList;
            setDataCount(data.count);
            if (_dataList.length > 0) {
                const _columns = extractKeys(_dataList[0]);
                // console.log("here: " + JSON.stringify(_columns));
                setColumns(_columns);
                setDataList(_dataList);
            }
        }).catch((err) => {
            let _dataList = mockData;
            setDataCount(200);
            if (_dataList.length > 0) {
                const _columns = extractKeys(_dataList[0]);
                console.log("here: " + JSON.stringify(_columns));
                setColumns(_columns);
                setDataList(_dataList);
            }
            message.error("Failed to query statistic data!")
        })
    }, [currentPage, selectedKey]);

    const handleSelectedKeyChange = (value) => {
        console.log(`selected ${value}`);
        setSelectedKey(value);
    };

    const handlePageChange = (page) => {
        setCurrentPage(page);
    };

    return (
        <Space direction="vertical" align="center" style={{ width: '100%' }}>
            <Select
                defaultValue={1}
                style={{
                    width: 300,
                }}
                onChange={handleSelectedKeyChange}
                options={options}
            />
            <Table 
                dataSource={dataList} 
                columns={columns} 
                pagination={{
                    position: ['bottomRight'],
                    showSizeChanger: false,
                    current: currentPage,
                    total: dataCount,
                    pageSize: 10,
                    onChange: handlePageChange,
                }}
            />
        </Space>
    );
}

export default Statistic;