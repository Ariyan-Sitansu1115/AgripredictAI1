import React, { useState } from 'react';
import {
  Box, Grid, Card, CardContent, Typography, Tabs, Tab, Avatar, Chip,
} from '@mui/material';
import SpaIcon from '@mui/icons-material/Spa';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import BarChartIcon from '@mui/icons-material/BarChart';
import RecommendIcon from '@mui/icons-material/Recommend';
import TimelineIcon from '@mui/icons-material/Timeline';
import NatureIcon from '@mui/icons-material/Nature';

import SoilHealthDashboard from '../components/Rotation/SoilHealthDashboard';
import RotationPlanner from '../components/Rotation/RotationPlanner';
import RotationTimeline from '../components/Rotation/RotationTimeline';
import HistoricalAnalytics from '../components/Rotation/HistoricalAnalytics';
import Recommendations from '../components/Rotation/Recommendations';
import RotationSummary from '../components/Rotation/RotationSummary';

// ── Tab definitions ──────────────────────────────────────────────────────────
const TABS = [
  { label: 'Overview',    icon: <NatureIcon /> },
  { label: 'Soil Health', icon: <SpaIcon /> },
  { label: 'Plan',        icon: <AutoAwesomeIcon /> },
  { label: 'Timeline',    icon: <TimelineIcon /> },
  { label: 'Analytics',   icon: <BarChartIcon /> },
  { label: 'Crops',       icon: <RecommendIcon /> },
];

// ── Feature highlights ───────────────────────────────────────────────────────
const FEATURES = [
  { icon: '🌱', title: 'Soil Health Tracking', desc: 'Real-time N, P, K, and organic matter monitoring' },
  { icon: '🔄', title: 'AI Rotation Engine', desc: 'Genetic-algorithm optimized multi-year schedules' },
  { icon: '💰', title: 'Profit Maximization', desc: 'Balance profitability with sustainability goals' },
  { icon: '🛡️', title: 'Pest Cycle Breaking', desc: 'Natural pest reduction through smart sequencing' },
];

function TabPanel({ children, value, index }) {
  return value === index ? <Box>{children}</Box> : null;
}

export default function CropRotation() {
  const [tab, setTab] = useState(0);
  const [generatedPlan, setGeneratedPlan] = useState(null);

  const handlePlanGenerated = (plan) => {
    setGeneratedPlan(plan);
    // Auto-navigate to timeline after plan generated
    setTimeout(() => setTab(3), 300);
  };

  return (
    <Box>
      {/* ── Hero Section ─────────────────────────────────────────────────── */}
      <Box
        sx={{
          background: 'linear-gradient(135deg, #065F46 0%, #10B981 60%, #34D399 100%)',
          borderRadius: 3,
          p: { xs: 2.5, sm: 4 },
          mb: 3,
          color: 'white',
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        {/* Decorative blobs */}
        <Box
          sx={{
            position: 'absolute', top: -40, right: -40,
            width: 180, height: 180,
            borderRadius: '50%',
            bgcolor: 'rgba(255,255,255,0.08)',
            pointerEvents: 'none',
          }}
        />
        <Box
          sx={{
            position: 'absolute', bottom: -30, right: 120,
            width: 100, height: 100,
            borderRadius: '50%',
            bgcolor: 'rgba(255,255,255,0.05)',
            pointerEvents: 'none',
          }}
        />

        <Grid container spacing={3} alignItems="center">
          <Grid item xs={12} md={7}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
              <Chip
                label="AI-Powered"
                size="small"
                sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white', fontWeight: 600 }}
              />
              <Chip
                label="New Feature"
                size="small"
                sx={{ bgcolor: '#F59E0B', color: 'white', fontWeight: 600 }}
              />
            </Box>
            <Typography variant="h4" fontWeight={700} mb={1} sx={{ lineHeight: 1.2 }}>
              🌾 Crop Rotation Planning
              <br />
              &amp; Soil Health Optimizer
            </Typography>
            <Typography variant="body1" sx={{ opacity: 0.9, maxWidth: 480 }}>
              AI-powered multi-year rotation planner that maintains soil health, maximizes
              profitability, and naturally reduces pest pressure on your farm.
            </Typography>
          </Grid>

          <Grid item xs={12} md={5}>
            <Grid container spacing={1.5}>
              {FEATURES.map((f) => (
                <Grid item xs={6} key={f.title}>
                  <Box
                    sx={{
                      p: 1.5,
                      bgcolor: 'rgba(255,255,255,0.12)',
                      borderRadius: 2,
                      backdropFilter: 'blur(8px)',
                      border: '1px solid rgba(255,255,255,0.2)',
                    }}
                  >
                    <Typography variant="h5" mb={0.5}>{f.icon}</Typography>
                    <Typography variant="body2" fontWeight={600} sx={{ lineHeight: 1.3 }}>
                      {f.title}
                    </Typography>
                    <Typography variant="caption" sx={{ opacity: 0.8 }}>{f.desc}</Typography>
                  </Box>
                </Grid>
              ))}
            </Grid>
          </Grid>
        </Grid>
      </Box>

      {/* ── Summary strip ─────────────────────────────────────────────────── */}
      <Box sx={{ mb: 3 }}>
        <RotationSummary plan={generatedPlan} />
      </Box>

      {/* ── Tab Navigation ────────────────────────────────────────────────── */}
      <Card sx={{ mb: 3 }}>
        <Tabs
          value={tab}
          onChange={(_, v) => setTab(v)}
          textColor="primary"
          indicatorColor="primary"
          variant="scrollable"
          scrollButtons="auto"
          sx={{ px: 2, pt: 1 }}
        >
          {TABS.map((t, i) => (
            <Tab
              key={t.label}
              label={t.label}
              icon={t.icon}
              iconPosition="start"
              sx={{
                fontSize: 13,
                fontWeight: tab === i ? 600 : 400,
                minHeight: 48,
                textTransform: 'none',
              }}
            />
          ))}
        </Tabs>
      </Card>

      {/* ── Tab Panels ────────────────────────────────────────────────────── */}
      <TabPanel value={tab} index={0}>
        {/* Overview: key stats + quick action cards */}
        <Grid container spacing={3}>
          {[
            { icon: '🌱', label: 'Soil Health Score', value: '74/100', sub: 'Moderate – improving', color: '#10B981' },
            { icon: '💰', label: 'Est. Revenue', value: '₹2.4L/ha', sub: 'Over 5-year cycle', color: '#F59E0B' },
            { icon: '🛡️', label: 'Pest Reduction', value: '42%', sub: 'vs. monoculture', color: '#8B5CF6' },
            { icon: '📈', label: 'Yield Improvement', value: '+18%', sub: 'Year-over-year', color: '#3B82F6' },
          ].map((s) => (
            <Grid item xs={6} sm={3} key={s.label}>
              <Card
                onClick={() => setTab(s.label.includes('Soil') ? 1 : s.label.includes('Revenue') ? 4 : s.label.includes('Pest') ? 5 : 4)}
                sx={{ cursor: 'pointer', textAlign: 'center' }}
              >
                <CardContent>
                  <Typography variant="h3" mb={1}>{s.icon}</Typography>
                  <Typography variant="h5" fontWeight={700} sx={{ color: s.color }}>{s.value}</Typography>
                  <Typography variant="body2" fontWeight={500}>{s.label}</Typography>
                  <Typography variant="caption" color="text.secondary">{s.sub}</Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}

          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" fontWeight={600} mb={1}>Getting Started</Typography>
                <Typography variant="body2" color="text.secondary" mb={2}>
                  Use the tabs above to navigate the Crop Rotation Optimizer. Here's a suggested workflow:
                </Typography>
                <Grid container spacing={2}>
                  {[
                    { step: '1', title: 'Check Soil Health', desc: 'Review your current N, P, K and organic matter levels', tab: 1 },
                    { step: '2', title: 'Generate Plan', desc: 'Fill the planner form to get your AI rotation schedule', tab: 2 },
                    { step: '3', title: 'View Timeline', desc: 'See the year-by-year rotation visualization', tab: 3 },
                    { step: '4', title: 'Explore Analytics', desc: 'Track historical performance and trends', tab: 4 },
                  ].map((item) => (
                    <Grid item xs={12} sm={6} md={3} key={item.step}>
                      <Box
                        onClick={() => setTab(item.tab)}
                        sx={{
                          p: 2,
                          bgcolor: '#F9FAFB',
                          borderRadius: 2,
                          cursor: 'pointer',
                          border: '1px solid #E5E7EB',
                          transition: 'all 0.2s',
                          '&:hover': { bgcolor: '#D1FAE5', borderColor: '#10B981' },
                        }}
                      >
                        <Avatar sx={{ bgcolor: 'primary.main', width: 28, height: 28, fontSize: 13, mb: 1 }}>
                          {item.step}
                        </Avatar>
                        <Typography variant="body2" fontWeight={600}>{item.title}</Typography>
                        <Typography variant="caption" color="text.secondary">{item.desc}</Typography>
                      </Box>
                    </Grid>
                  ))}
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      <TabPanel value={tab} index={1}>
        <SoilHealthDashboard />
      </TabPanel>

      <TabPanel value={tab} index={2}>
        <RotationPlanner onPlanGenerated={handlePlanGenerated} />
      </TabPanel>

      <TabPanel value={tab} index={3}>
        <RotationTimeline plan={generatedPlan} />
      </TabPanel>

      <TabPanel value={tab} index={4}>
        <HistoricalAnalytics />
      </TabPanel>

      <TabPanel value={tab} index={5}>
        <Recommendations />
      </TabPanel>
    </Box>
  );
}
