import * as Yup from 'yup';
import { useFormik, Form, FormikProvider } from 'formik';
import { styled } from '@mui/material/styles';
import { Container, Typography, Stack, TextField } from '@mui/material';
import { LoadingButton } from '@mui/lab';
import UserDataService from "../utilities/UserDataService";

// import { Chip } from '@mui/material';
// import { MenuItem } from '@mui/material';

import { useState } from 'react';

const ContentStyle = styled('div')(({ theme }) => ({
    maxWidth: 800,
    margin: 'auto',
    minHeight: '100vh',
    display: 'flex',
    justifyContent: 'center',
    flexDirection: 'column',
    padding: theme.spacing(12, 0),
}));

// const property_types = ["Apartment", "House", "Villa", "Cabin", "Hotel", "Guesthouse", "Cave", "Farm"];
// const property_options = {
//     "Apartment": ["An entire place", "A room", "A shared room"],
//     "House": ["An entire place", "A room", "A shared room"],
//     "Villa": ["An entire place", "A room", "A shared room"],
//     "Cabin": ["An entire place", "A room"],
//     "Hotel": ["An entire place", "A room", "A shared room"],
//     "Guesthouse": ["An entire place", "A room", "A shared room"],
//     "Cave": ["An entire place", "A room", "A shared room"],
//     "Farm": ["An entire place", "A room", "A shared room"]
// };

// const amenitiesCollection = [
//     "piano", "TV", "WiFi", "beach access", "dedicated wokplacepool",
//     "smoke alarm", "Free parking on premises", "kitchenSwimming Pool",
//     "fire extinguisher", "paid parking on premises", "Kitchen"
// ];

// const bed_types = ["Single", "Double", "Queen", "King"];
// const neighborhoods = ["Downtown", "Suburb", "Waterfront", "Mountain View"];
// const guest_types = ["Any Airbnb guest", "An experienced guest"];

export default function CreateUserForm() {

    const [sentiment, setSentiment] = useState('');
    const [suggestedPrice, setSuggestedPrice] = useState('');
    const [nearestPrice, setNearestPrice] = useState('');

    const UserSchema = Yup.object().shape({
        location: Yup.string().required('Location is required'),
        latitude: Yup.number().typeError('Latitude must be a number').required('Latitude is required'),
        longitude: Yup.number().typeError('Longitude must be a number').required('Longitude is required'),
        property_type: Yup.string().required('Property type is required'),
        option: Yup.string().required('Option is required'),
        guests: Yup.number().integer().min(1).required('Number of guests is required'),
        number_of_bedrooms: Yup.number().integer().min(1).required('Number of bedrooms is required'),
        amenities: Yup.array().of(Yup.string()).min(1, 'At least one amenity is required').required('At least one amenity is required'),
        seasonality: Yup.string().required('Seasonality is required'),
        base_price: Yup.number().min(50).required('Base price is required'),
        bathrooms: Yup.number().integer().min(1).required('Number of bathrooms is required'),
        bed_type: Yup.string().required('Bed type is required'),
        beds: Yup.number().integer().min(1).required('Number of beds is required'),
        neighborhood: Yup.string().required('Neighborhood is required'),
        guest_type: Yup.string().required('Guest type is required'),
        title: Yup.string().required('Title is required'),
        description: Yup.string().required('Description is required'),

    });

    const formik = useFormik({
        initialValues: {
            location: '',
            latitude: '',
            longitude: '',
            property_type: '',
            option: '',
            guests: '',
            number_of_bedrooms: '',
            amenities: [],
            seasonality: '',
            base_price: '',
            bathrooms: '',
            bed_type: '',
            beds: '',
            neighborhood: '',
            guest_type: '',
            description: '',
            title: '',

        },
        validationSchema: UserSchema,
        onSubmit: (values) => {
            console.log(values);
            UserDataService.create(values)
                .then((res) => {
                    setSubmitting(false);
                    console.log('Suggested price created successfully.');

                    // Fetch the results after successful submission
                    // fetchResultsFromBackend(values.description);

                    fetchResultsFromBackend(
                        values.location,
                        values.latitude,
                        values.longitude,
                        values.property_type,
                        values.option,
                        values.guests,
                        values.number_of_bedrooms,
                        values.amenities, // No need to split here
                        values.seasonality,
                        values.base_price,
                        values.bathrooms,
                        values.bed_type,
                        values.beds,
                        values.neighborhood,
                        values.guest_type,
                        values.description,
                        values.title
                    );
                })
                // .catch(e => {
                //     console.log(e);

                .catch((e) => {
                    setSubmitting(false);
                    formik.setFieldError('review', 'You are already created');
                    console.log(e);
                });
        }
    });

    function fetchResultsFromBackend(location, latitude, longitude, property_type, option, guests, number_of_bedrooms, amenities, seasonality, base_price, bathrooms, bed_type, beds, neighborhood, guest_type, description, title) {

        // const amenitiesArray = amenities.split(',').map(item => item.trim());

        fetch('http://localhost:5051/predict', {
            method: 'POST',
            // method: 'OPTION',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({

                location: location,
                // latitude: latitude,
                // longitude: longitude,
                latitude: latitude !== null ? parseFloat(latitude) : null,
                longitude: longitude !== null ? parseFloat(longitude) : null,
                property_type: property_type,
                option: option,
                guests: guests,
                number_of_bedrooms: number_of_bedrooms,
                amenities: amenities,
                // amenities: amenitiesArray,
                seasonality: seasonality,
                base_price: base_price,
                bathrooms: bathrooms,
                bed_type: bed_type,
                beds: beds,
                neighborhood: neighborhood,
                guest_type: guest_type,
                description: description,
                title: title

            }),
        })
            .then((response) => response.json())
            .then((data) => {
                console.log('Received prediction data:', data);
                setSentiment(data.sentiment);
                setSuggestedPrice(data.suggested_price);
                setNearestPrice(data.nearest_price);
            })
            .catch((error) => {
                console.error('Error fetching results:', error);
            });
    }

    const { errors, touched, handleSubmit, isSubmitting, setSubmitting, getFieldProps } = formik;

    // const { errors, touched, handleSubmit, isSubmitting, setSubmitting, getFieldProps, handleBlur, values } = formik;

    return (
        <Container>
            <ContentStyle>
                <Typography variant="h4" gutterBottom>
                    Create your own host
                </Typography>
                <Typography sx={{ color: 'text.secondary', mb: 5 }}>Welcome to our host zone</Typography>
                <FormikProvider value={formik}>
                    <Form autoComplete="off" noValidate onSubmit={handleSubmit}>
                        <Stack spacing={3}>
                            <TextField
                                fullWidth
                                autoComplete="location"
                                type="text"
                                label="Location"
                                {...getFieldProps('location')}
                                error={Boolean(touched.location && errors.location)}
                                helperText={touched.location && errors.location}
                            />

                            <TextField
                                fullWidth
                                autoComplete="latitude"
                                type="number"
                                label="Latitude"
                                {...getFieldProps('latitude')}
                                error={Boolean(touched.latitude && errors.latitude)}
                                helperText={touched.latitude && errors.latitude}
                            />

                            <TextField
                                fullWidth
                                autoComplete="longitude"
                                type="number"
                                label="Longitude"
                                {...getFieldProps('longitude')}
                                error={Boolean(touched.longitude && errors.longitude)}
                                helperText={touched.longitude && errors.longitude}
                            />

                            <TextField
                                fullWidth
                                autoComplete="property_type"
                                type="text"
                                label="Property Type"
                                {...getFieldProps('property_type')}
                                error={Boolean(touched.property_type && errors.property_type)}
                                helperText={touched.property_type && errors.property_type}
                            />

                            <TextField
                                fullWidth
                                autoComplete="option"
                                type="text"
                                label="Option"
                                {...getFieldProps('option')}
                                error={Boolean(touched.option && errors.option)}
                                helperText={touched.option && errors.option}
                            />

                            <TextField
                                fullWidth
                                autoComplete="guests"
                                type="number"
                                label="Guests"
                                {...getFieldProps('guests')}
                                error={Boolean(touched.guests && errors.guests)}
                                helperText={touched.guests && errors.guests}
                            />

                            <TextField
                                fullWidth
                                autoComplete="number_of_bedrooms"
                                type="number"
                                label="Number of Bedrooms"
                                {...getFieldProps('number_of_bedrooms')}
                                error={Boolean(touched.number_of_bedrooms && errors.number_of_bedrooms)}
                                helperText={touched.number_of_bedrooms && errors.number_of_bedrooms}
                            />

                            <TextField
                                fullWidth
                                autoComplete="amenities"
                                type="text"
                                label="Amenities"
                                {...getFieldProps('amenities')}
                                error={Boolean(touched.amenities && errors.amenities)}
                                helperText={touched.amenities && errors.amenities}
                                onBlur={(event) => {
                                    const amenitiesArray = event.target.value.split(',').map(item => item.trim());
                                    formik.setFieldValue('amenities', amenitiesArray);
                                    formik.handleBlur(event);
                                }}
                            />

                            <TextField
                                fullWidth
                                autoComplete="seasonality"
                                type="text"
                                label="Seasonality"
                                {...getFieldProps('seasonality')}
                                error={Boolean(touched.seasonality && errors.seasonality)}
                                helperText={touched.seasonality && errors.seasonality}
                            />

                            <TextField
                                fullWidth
                                autoComplete="base_price"
                                type="number"
                                label="Base Price"
                                {...getFieldProps('base_price')}
                                error={Boolean(touched.base_price && errors.base_price)}
                                helperText={touched.base_price && errors.base_price}
                            />

                            <TextField
                                fullWidth
                                autoComplete="bathrooms"
                                type="number"
                                label="Bathrooms"
                                {...getFieldProps('bathrooms')}
                                error={Boolean(touched.bathrooms && errors.bathrooms)}
                                helperText={touched.bathrooms && errors.bathrooms}
                            />

                            <TextField
                                fullWidth
                                autoComplete="bed_type"
                                type="text"
                                label="Bed Type"
                                {...getFieldProps('bed_type')}
                                error={Boolean(touched.bed_type && errors.bed_type)}
                                helperText={touched.bed_type && errors.bed_type}
                            />

                            <TextField
                                fullWidth
                                autoComplete="beds"
                                type="number"
                                label="Beds"
                                {...getFieldProps('beds')}
                                error={Boolean(touched.beds && errors.beds)}
                                helperText={touched.beds && errors.beds}
                            />

                            <TextField
                                fullWidth
                                autoComplete="neighborhood"
                                type="text"
                                label="Neighborhood"
                                {...getFieldProps('neighborhood')}
                                error={Boolean(touched.neighborhood && errors.neighborhood)}
                                helperText={touched.neighborhood && errors.neighborhood}
                            />

                            <TextField
                                fullWidth
                                autoComplete="guest_type"
                                type="text"
                                label="Guest Type"
                                {...getFieldProps('guest_type')}
                                error={Boolean(touched.guest_type && errors.guest_type)}
                                helperText={touched.guest_type && errors.guest_type}
                            />

                            <TextField
                                fullWidth
                                autoComplete="title"
                                type="text"
                                label="Title"
                                {...getFieldProps('title')}
                                error={Boolean(touched.title && errors.title)}
                                helperText={touched.title && errors.title}
                            />

                            <TextField
                                fullWidth
                                autoComplete="description"
                                type="text"
                                label="Description"
                                {...getFieldProps('description')}
                                error={Boolean(touched.description && errors.description)}
                                helperText={touched.description && errors.description}
                            />
                            <LoadingButton fullWidth size="large" type="submit" variant="contained" loading={isSubmitting}>
                                Save Details
                            </LoadingButton>

                            <Typography variant="h6">Sentiment: {sentiment}</Typography>
                            {/* <Typography variant="h6">Predicted Price: {predictedPrice}</Typography> */}
                            <Typography variant="h6">Suggested Price: {suggestedPrice}</Typography>
                            <Typography variant="h6">Nearest Price: {nearestPrice}</Typography>

                        </Stack>
                    </Form>
                </FormikProvider>
            </ContentStyle>
        </Container>
    );
}