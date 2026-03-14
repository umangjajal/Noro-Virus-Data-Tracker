from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

class CasesApiTests(APITestCase):
    
    @patch('cases.views.get_db')
    def test_global_stats_structure(self, mock_get_db):
        # Mocking MongoDB response
        mock_db = mock_get_db.return_value
        mock_db['cases'].count_documents.side_effect = [100, 10, 80] # Total, Dead, Recovered
        
        url = reverse('global-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_cases', response.data)
        self.assertIn('active_cases', response.data)
        self.assertEqual(response.data['active_cases'], 10) # 100 - 10 - 80

    @patch('cases.views.get_db')
    def test_comorbidity_stats_structure(self, mock_get_db):
        mock_db = mock_get_db.return_value
        mock_db['cases'].count_documents.return_value = 5
        
        url = reverse('comorbidity-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['diabetes_cases'], 5)

    def test_swagger_docs_load(self):
        url = reverse('swagger-ui')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
