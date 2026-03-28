import { useState, useEffect, useCallback } from 'react';
import { getPricePredictions } from '../services/predictionService';
import { PricePrediction } from '../types';

const MOCK_PREDICTIONS: PricePrediction[] = [
  {
    id: '1',
    crop: 'Wheat',
    currentPrice: 425,
    predictedPrice: 448,
    confidence: 87,
    trend: 'up',
    period: '30 days',
    priceHistory: Array.from({ length: 30 }, (_, i) => ({
      date: new Date(Date.now() - (29 - i) * 86400000).toISOString().split('T')[0],
      actual: i < 25 ? 400 + Math.random() * 50 : undefined,
      predicted: i >= 20 ? 420 + Math.random() * 40 : undefined,
    })),
  },
  {
    id: '2',
    crop: 'Rice',
    currentPrice: 380,
    predictedPrice: 365,
    confidence: 82,
    trend: 'down',
    period: '30 days',
    priceHistory: Array.from({ length: 30 }, (_, i) => ({
      date: new Date(Date.now() - (29 - i) * 86400000).toISOString().split('T')[0],
      actual: i < 25 ? 390 - Math.random() * 20 : undefined,
      predicted: i >= 20 ? 375 - Math.random() * 15 : undefined,
    })),
  },
  {
    id: '3',
    crop: 'Corn',
    currentPrice: 290,
    predictedPrice: 305,
    confidence: 79,
    trend: 'up',
    period: '30 days',
    priceHistory: Array.from({ length: 30 }, (_, i) => ({
      date: new Date(Date.now() - (29 - i) * 86400000).toISOString().split('T')[0],
      actual: i < 25 ? 280 + Math.random() * 25 : undefined,
      predicted: i >= 20 ? 295 + Math.random() * 20 : undefined,
    })),
  },
];

export const usePredictions = (crop?: string) => {
  const [predictions, setPredictions] = useState<PricePrediction[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchPredictions = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await getPricePredictions(crop);
      setPredictions(data);
    } catch (err) {
      console.error('Failed to fetch predictions:', err);
      setPredictions(MOCK_PREDICTIONS.filter(p => !crop || p.crop === crop));
    } finally {
      setIsLoading(false);
    }
  }, [crop]);

  useEffect(() => {
    fetchPredictions();
  }, [fetchPredictions]);

  const filterByCrop = useCallback(
    (cropName: string) => predictions.filter(p => p.crop === cropName),
    [predictions]
  );

  const getByConfidence = useCallback(
    (minConfidence: number) => predictions.filter(p => p.confidence >= minConfidence),
    [predictions]
  );

  return { predictions, isLoading, error, fetchPredictions, filterByCrop, getByConfidence };
};
