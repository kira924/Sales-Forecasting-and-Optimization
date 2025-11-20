import React, { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';
import { formatCurrency, formatPercentage } from '../../utils/helpers';
import { RISK_LEVELS } from '../../utils/constants';

const RankingTable = ({ data }) => {
  const [expandedRow, setExpandedRow] = useState(null);
  const [sortField, setSortField] = useState('rank');
  const [sortDirection, setSortDirection] = useState('asc');

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };

  const sortedData = [...data].sort((a, b) => {
    let aVal = a[sortField];
    let bVal = b[sortField];
    
    if (sortField === 'rank') {
      aVal = data.indexOf(a);
      bVal = data.indexOf(b);
    }
    
    if (sortDirection === 'asc') {
      return aVal > bVal ? 1 : -1;
    } else {
      return aVal < bVal ? 1 : -1;
    }
  });

  const getRiskBadge = (risk) => {
    const config = RISK_LEVELS[risk];
    return (
      <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold bg-${config.color} bg-opacity-20 text-${config.color}`}>
        {config.emoji} {config.label}
      </span>
    );
  };

  const SortIcon = ({ field }) => {
    if (sortField !== field) return null;
    return sortDirection === 'asc' ? (
      <ChevronUp className="w-4 h-4 inline ml-1" />
    ) : (
      <ChevronDown className="w-4 h-4 inline ml-1" />
    );
  };

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b-2 border-gray-200">
            <th 
              className="text-left py-3 px-4 font-semibold text-gray-500 cursor-pointer hover:text-secondary"
              onClick={() => handleSort('rank')}
            >
              Rank <SortIcon field="rank" />
            </th>
            <th 
              className="text-left py-3 px-4 font-semibold text-gray-500 cursor-pointer hover:text-secondary"
              onClick={() => handleSort('make')}
            >
              Car Make <SortIcon field="make" />
            </th>
            <th className="text-left py-3 px-4 font-semibold text-gray-500">Model</th>
            <th className="text-center py-3 px-4 font-semibold text-gray-500">Year</th>
            <th className="text-center py-3 px-4 font-semibold text-gray-500">Qty</th>
            <th 
              className="text-right py-3 px-4 font-semibold text-gray-500 cursor-pointer hover:text-secondary"
              onClick={() => handleSort('profit')}
            >
              Profit <SortIcon field="profit" />
            </th>
            <th 
              className="text-center py-3 px-4 font-semibold text-gray-500 cursor-pointer hover:text-secondary"
              onClick={() => handleSort('confidence')}
            >
              Conf. <SortIcon field="confidence" />
            </th>
            <th 
              className="text-center py-3 px-4 font-semibold text-gray-500 cursor-pointer hover:text-secondary"
              onClick={() => handleSort('risk')}
            >
              Risk <SortIcon field="risk" />
            </th>
            <th className="text-center py-3 px-4 font-semibold text-gray-500">Action</th>
          </tr>
        </thead>
        <tbody>
          {sortedData.map((car, index) => (
            <React.Fragment key={index}>
              <tr 
                className="border-b border-gray-100 hover:bg-gray-50 transition-colors cursor-pointer"
                onClick={() => setExpandedRow(expandedRow === index ? null : index)}
              >
                <td className="py-3 px-4">
                  <span className="font-bold text-secondary">#{data.indexOf(car) + 1}</span>
                </td>
                <td className="py-3 px-4 font-semibold text-primary">{car.make}</td>
                <td className="py-3 px-4 text-gray-500">{car.model}</td>
                <td className="py-3 px-4 text-center text-gray-500">{car.year}</td>
                <td className="py-3 px-4 text-center text-gray-500">{car.quantity}</td>
                <td className="py-3 px-4 text-right font-mono font-semibold text-primary">
                  {formatCurrency(car.profit)}
                </td>
                <td className="py-3 px-4 text-center">
                  <span className={`font-semibold ${car.confidence > 50 ? 'text-success' : car.confidence > 30 ? 'text-warning' : 'text-danger'}`}>
                    {formatPercentage(car.confidence, 0)}
                  </span>
                </td>
                <td className="py-3 px-4 text-center">
                  {getRiskBadge(car.risk)}
                </td>
                <td className="py-3 px-4 text-center">
                  <button className="text-secondary hover:text-secondary-dark transition-colors">
                    {expandedRow === index ? (
                      <ChevronUp className="w-5 h-5" />
                    ) : (
                      <ChevronDown className="w-5 h-5" />
                    )}
                  </button>
                </td>
              </tr>
              
              {/* Expanded Details */}
              {expandedRow === index && (
                <tr className="bg-gray-50 border-b border-gray-200">
                  <td colSpan="9" className="py-4 px-6">
                    <div className="space-y-3">
                      <h4 className="font-semibold text-primary">
                         {car.make} {car.model} ({car.year}) - Detailed Analysis
                      </h4>
                      
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                        <div className="space-y-2">
                          <p><strong className="text-gray-500">Predicted Profit:</strong> <span className="text-primary font-semibold">{formatCurrency(car.profit)}</span></p>
                          <p><strong className="text-gray-500">Confidence:</strong> <span className="text-primary">{formatPercentage(car.confidence)}%</span></p>
                          <p><strong className="text-gray-500">Car Age:</strong> <span className="text-primary">{car.age} years</span></p>
                        </div>
                        
                        <div className="space-y-2">
                          <p><strong className="text-gray-500">Risk Level:</strong> {getRiskBadge(car.risk)}</p>
                          <p className="text-gray-400">
                            {car.risk === 'LOW' && ' Strong buy - High profit potential with low risk'}
                            {car.risk === 'MEDIUM' && ' Moderate risk - Consider market conditions'}
                            {car.risk === 'HIGH' && ' High risk - Only purchase with specific demand'}
                          </p>
                        </div>
                      </div>
                    </div>
                  </td>
                </tr>
              )}
            </React.Fragment>
          ))}
        </tbody>
      </table>

      <div className="mt-4 text-xs text-gray-400 italic">
         Click on any row to see detailed analysis
      </div>
    </div>
  );
};

export default RankingTable;