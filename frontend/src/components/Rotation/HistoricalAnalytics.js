import React, { useState } from 'react';
import {
  Box, Grid, Card, CardContent, Typography, Tabs, Tab,
  Chip, Button,
} from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';
import {
  LineChart, Line, AreaChart, Area, BarChart, Bar,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell,
} from 'recharts';

// ── Mock data ────────────────────────────────────────────────────────────────
const SOIL_TREND = [
  { year: '2020', score: 58, nitrogen: 38, phosphorus: 15 },
  { year: '2021', score: 62, nitrogen: 40, phosphorus: 17 },
  { year: '2022', score: 65, nitrogen: 42, phosphorus: 19 },
  { year: '2023', score: 70, nitrogen: 44, phosphorus: 21 },
  { year: '2024', score: 74, nitrogen: 45, phosphorus: 22 },
];

const YIELD_DATA = [
  { crop: 'Rice', '2022': 4.5, '2023': 4.8, '2024': 5.0 },
  { crop: 'Wheat', '2022': 3.8, '2023': 4.0, '2024': 4.2 },
  { crop: 'Maize', '2022': 5.8, '2023': 6.1, '2024': 6.5 },
  { crop: 'Chickpea', '2022': 1.5, '2023': 1.6, '2024': 1.8 },
];

const PROFIT_DATA = [
  { month: 'Jan', profit: 42000 },
  { month: 'Feb', profit: 38000 },
  { month: 'Mar', profit: 55000 },
  { month: 'Apr', profit: 61000 },
  { month: 'May', profit: 58000 },
  { month: 'Jun', profit: 47000 },
  { month: 'Jul', profit: 52000 },
  { month: 'Aug', profit: 68000 },
  { month: 'Sep', profit: 72000 },
  { month: 'Oct', profit: 65000 },
  { month: 'Nov', profit: 78000 },
  { month: 'Dec', profit: 82000 },
];

const ROTATION_HISTORY = [
  { id: 1, year: 2020, crop: 'Rice', area: 5, yield: '4.5 t/ha', profit: '₹45,000', soilScore: 58 },
  { id: 2, year: 2021, crop: 'Wheat', area: 5, yield: '4.0 t/ha', profit: '₹40,000', soilScore: 62 },
  { id: 3, year: 2022, crop: 'Chickpea', area: 5, yield: '1.6 t/ha', profit: '₹32,000', soilScore: 65 },
  { id: 4, year: 2023, crop: 'Maize', area: 5, yield: '6.1 t/ha', profit: '₹61,000', soilScore: 70 },
  { id: 5, year: 2024, crop: 'Mustard', area: 5, yield: '1.5 t/ha', profit: '₹28,000', soilScore: 74 },
];

const CROP_DISTRIBUTION = [
  { name: 'Rice', value: 30, color: '#10B981' },
  { name: 'Wheat', value: 25, color: '#F59E0B' },
  { name: 'Maize', value: 20, color: '#8B5CF6' },
  { name: 'Legumes', value: 15, color: '#3B82F6' },
  { name: 'Others', value: 10, color: '#EF4444' },
];

function TabPanel({ value, index, children }) {
  return value === index ? <Box sx={{ pt: 2 }}>{children}</Box> : null;
}

function formatINR(value) {
  return `₹${(value / 1000).toFixed(0)}K`;
}

export default function HistoricalAnalytics() {
  const [tab, setTab] = useState(0);

  const handleExport = () => {
    const header = 'Year,Crop,Area (ha),Yield,Profit,Soil Score\n';
    const rows = ROTATION_HISTORY.map(
      (r) => `${r.year},${r.crop},${r.area},${r.yield},${r.profit},${r.soilScore}`
    ).join('\n');
    const blob = new Blob([header + rows], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'rotation_history.csv';
    link.click();
    URL.revokeObjectURL(url);
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
        <Tabs
          value={tab}
          onChange={(_, v) => setTab(v)}
          textColor="primary"
          indicatorColor="primary"
          variant="scrollable"
          scrollButtons="auto"
        >
          <Tab label="Rotation History" />
          <Tab label="Soil Quality" />
          <Tab label="Yield Performance" />
          <Tab label="Profitability" />
          <Tab label="Crop Distribution" />
        </Tabs>
        <Button
          variant="outlined"
          size="small"
          startIcon={<DownloadIcon />}
          onClick={handleExport}
          sx={{ ml: 1, flexShrink: 0 }}
        >
          Export CSV
        </Button>
      </Box>

      {/* Rotation History */}
      <TabPanel value={tab} index={0}>
        <Card>
          <CardContent>
            <Typography variant="h6" fontWeight={600} mb={2}>Rotation History</Typography>
            <Box sx={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 14 }}>
                <thead>
                  <tr style={{ borderBottom: '2px solid #E5E7EB' }}>
                    {['Year', 'Crop', 'Area (ha)', 'Yield', 'Profit', 'Soil Score'].map((h) => (
                      <th key={h} style={{ padding: '8px 12px', textAlign: 'left', color: '#6B7280', fontWeight: 600 }}>
                        {h}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {ROTATION_HISTORY.map((row, i) => (
                    <tr
                      key={row.id}
                      style={{ borderBottom: '1px solid #F3F4F6', backgroundColor: i % 2 === 0 ? '#FAFAFA' : '#FFF' }}
                    >
                      <td style={{ padding: '10px 12px', fontWeight: 600 }}>{row.year}</td>
                      <td style={{ padding: '10px 12px' }}>
                        <Chip label={row.crop} size="small" sx={{ bgcolor: '#D1FAE5', color: '#065F46' }} />
                      </td>
                      <td style={{ padding: '10px 12px' }}>{row.area}</td>
                      <td style={{ padding: '10px 12px' }}>{row.yield}</td>
                      <td style={{ padding: '10px 12px', color: '#10B981', fontWeight: 600 }}>{row.profit}</td>
                      <td style={{ padding: '10px 12px' }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Box
                            sx={{
                              width: 48,
                              height: 6,
                              borderRadius: 3,
                              bgcolor: '#E5E7EB',
                              overflow: 'hidden',
                            }}
                          >
                            <Box
                              sx={{
                                width: `${row.soilScore}%`,
                                height: '100%',
                                bgcolor: row.soilScore >= 70 ? '#10B981' : row.soilScore >= 55 ? '#F59E0B' : '#EF4444',
                              }}
                            />
                          </Box>
                          <Typography variant="caption">{row.soilScore}</Typography>
                        </Box>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </Box>
          </CardContent>
        </Card>
      </TabPanel>

      {/* Soil Quality Trends */}
      <TabPanel value={tab} index={1}>
        <Card>
          <CardContent>
            <Typography variant="h6" fontWeight={600} mb={2}>Soil Quality Trends (5 Years)</Typography>
            <ResponsiveContainer width="100%" height={320}>
              <AreaChart data={SOIL_TREND} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>
                <defs>
                  <linearGradient id="scoreGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10B981" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#10B981" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#F3F4F6" />
                <XAxis dataKey="year" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip contentStyle={{ borderRadius: 8, border: '1px solid #E5E7EB', fontSize: 12 }} />
                <Legend />
                <Area type="monotone" dataKey="score" stroke="#10B981" fill="url(#scoreGrad)" name="Health Score" strokeWidth={2} />
                <Line type="monotone" dataKey="nitrogen" stroke="#F59E0B" name="Nitrogen (ppm)" strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="phosphorus" stroke="#8B5CF6" name="Phosphorus (ppm)" strokeWidth={2} dot={false} />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </TabPanel>

      {/* Yield Performance */}
      <TabPanel value={tab} index={2}>
        <Card>
          <CardContent>
            <Typography variant="h6" fontWeight={600} mb={2}>Yield Performance (t/ha)</Typography>
            <ResponsiveContainer width="100%" height={320}>
              <BarChart data={YIELD_DATA} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#F3F4F6" />
                <XAxis dataKey="crop" tick={{ fontSize: 12 }} />
                <YAxis tick={{ fontSize: 12 }} />
                <Tooltip contentStyle={{ borderRadius: 8, border: '1px solid #E5E7EB', fontSize: 12 }} />
                <Legend />
                <Bar dataKey="2022" fill="#8B5CF6" name="2022" radius={[4, 4, 0, 0]} />
                <Bar dataKey="2023" fill="#F59E0B" name="2023" radius={[4, 4, 0, 0]} />
                <Bar dataKey="2024" fill="#10B981" name="2024" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </TabPanel>

      {/* Profitability */}
      <TabPanel value={tab} index={3}>
        <Card>
          <CardContent>
            <Typography variant="h6" fontWeight={600} mb={2}>Profitability History (₹ / month)</Typography>
            <ResponsiveContainer width="100%" height={320}>
              <LineChart data={PROFIT_DATA} margin={{ top: 10, right: 20, left: 10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#F3F4F6" />
                <XAxis dataKey="month" tick={{ fontSize: 12 }} />
                <YAxis tickFormatter={formatINR} tick={{ fontSize: 12 }} />
                <Tooltip formatter={(v) => [`₹${v.toLocaleString('en-IN')}`, 'Profit']}
                  contentStyle={{ borderRadius: 8, border: '1px solid #E5E7EB', fontSize: 12 }} />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="profit"
                  stroke="#10B981"
                  strokeWidth={2}
                  name="Profit (₹)"
                  dot={{ r: 4 }}
                  activeDot={{ r: 6 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </TabPanel>

      {/* Crop Distribution */}
      <TabPanel value={tab} index={4}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" fontWeight={600} mb={2}>Crop Rotation Distribution</Typography>
                <ResponsiveContainer width="100%" height={280}>
                  <PieChart>
                    <Pie
                      data={CROP_DISTRIBUTION}
                      cx="50%"
                      cy="50%"
                      outerRadius={100}
                      dataKey="value"
                      label={({ name, value }) => `${name} ${value}%`}
                      labelLine
                    >
                      {CROP_DISTRIBUTION.map((entry) => (
                        <Cell key={entry.name} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip contentStyle={{ borderRadius: 8, border: '1px solid #E5E7EB', fontSize: 12 }} />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Typography variant="h6" fontWeight={600} mb={2}>Distribution Breakdown</Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  {CROP_DISTRIBUTION.map((item) => (
                    <Box key={item.name}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                        <Typography variant="body2" fontWeight={500}>{item.name}</Typography>
                        <Typography variant="body2" fontWeight={600} sx={{ color: item.color }}>
                          {item.value}%
                        </Typography>
                      </Box>
                      <Box sx={{ height: 8, bgcolor: '#E5E7EB', borderRadius: 4, overflow: 'hidden' }}>
                        <Box sx={{ width: `${item.value}%`, height: '100%', bgcolor: item.color, borderRadius: 4 }} />
                      </Box>
                    </Box>
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>
    </Box>
  );
}
