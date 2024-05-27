import { useEffect, useState } from "react";
import { Input, Select, Space, Tag, Table, message } from 'antd';
import { postSearch } from "../requests/api";
import { extractKeys } from "../utils/CommonUtils";
const { Search } = Input;

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

const options = [
    {
        value: 'Mammal',
        label: 'Mammal',
    },
    {
        value: 'Country',
        label: 'Country',
    },
    {
        value: 'Continent',
        label: 'Continent',
    },
    {
        value: 'Institution',
        label: 'Institution',
    },
    {
        value: 'Publication',
        label: 'Publication',
    }
]

function Home() {

	const [dataList, setDataList] = useState([]);
	const [columns, setColumns] = useState([]);
	const [currentPage, setCurrentPage] = useState(1);
	const [dataCount, setDataCount] = useState(0);
	const [selectedKey, setSelectedKey] = useState('Mammal');
	const [searchText, setSearchText] = useState('');

	const handleSelectedKeyChange = (value) => {
		// console.log(`selected ${value}`);
		setSelectedKey(value);
	};

    const handlePageChange = (page) => {
        setCurrentPage(page);
    };

    useEffect(() => {
        postSearch({
            type: selectedKey,
			query: searchText,
			page: currentPage,
        }).then((data) => {
            let _dataList = data.dataList;
            setDataCount(data.count);
            if (_dataList.length > 0) {
                const _columns = extractKeys(_dataList[0]);
                setColumns(_columns);
                setDataList(_dataList);
            }
        }).catch((err) => {
            // let _dataList = mockData;
            // setDataCount(200);
            // if (_dataList.length > 0) {
            //     const _columns = extractKeys(_dataList[0]);
            //     // console.log("here: " + JSON.stringify(_columns));
            //     setColumns(_columns);
            //     setDataList(_dataList);
            // }
            message.error("Failed to query data!")
        })
    }, [currentPage]);
	
	const handleSearch = (value, _e, info) => {
		// console.log(info?.source, value);
		postSearch({
			type: selectedKey,
			query: searchText,
			page: currentPage,
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
            // let _dataList = mockData;
            // setDataCount(200);
            // if (_dataList.length > 0) {
            //     const _columns = extractKeys(_dataList[0]);
            //     console.log("here: " + JSON.stringify(_columns));
            //     setColumns(_columns);
            //     setDataList(_dataList);
            // }
            message.error("Failed to query data!")
		})
	};

    const handleSearchTextChange = (e) => {
        // console.log("searchText: " + e.target.value);
        setSearchText(e.target.value);
    }

    return (
        <Space direction='vertical' align='center' size='large'>
            <Space align='center' size='middle'>
				<Select
					defaultValue="Mammal"
					style={{
						width: 100, margin: 8
					}}
					onChange={handleSelectedKeyChange}
					options={options}
				/>
            <Search 
                style={{ width: 400 }} 
                placeholder="input search text" 
                size="large" 
                onSearch={handleSearch}
                onChange={handleSearchTextChange}
                enterButton 
            />
            </Space>
            <Table 
                columns={columns} 
                dataSource={dataList}
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

export default Home;