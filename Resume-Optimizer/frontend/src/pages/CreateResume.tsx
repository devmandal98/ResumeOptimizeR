import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useForm, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Plus, Minus, Download, Eye } from 'lucide-react';
import { PDFDocument, StandardFonts, rgb } from 'pdf-lib';
import { saveAs } from 'file-saver';


const resumeSchema = z.object({
  template: z.string().min(1, 'Please select a template'),
  personalInfo: z.object({
    fullName: z.string().min(1, 'Full name is required'),
    email: z.string().email('Invalid email address'),
    phone: z.string().min(1, 'Phone number is required'),
    linkedin: z.string().optional(),
    website: z.string().optional(),
  }),
  summary: z.string().min(10, 'Please provide a brief summary'),
  experience: z.array(z.object({
    jobTitle: z.string().min(1, 'Job title is required'),
    company: z.string().min(1, 'Company name is required'),
    startDate: z.string().min(1, 'Start date is required'),
    endDate: z.string(),
    description: z.string().min(1, 'Job description is required'),
  })),
  education: z.array(z.object({
    degree: z.string().min(1, 'Degree is required'),
    school: z.string().min(1, 'School name is required'),
    graduationDate: z.string().min(1, 'Graduation date is required'),
    achievements: z.string().optional(),
  })),
  skills: z.object({
    technical: z.array(z.string()).min(1, 'Add at least one technical skill'),
    soft: z.array(z.string()).min(1, 'Add at least one soft skill'),
  }),
  certifications: z.array(z.object({
    name: z.string().min(1, 'Certification name is required'),
    issuer: z.string().min(1, 'Issuing organization is required'),
    date: z.string().min(1, 'Date is required'),
  })),
  languages: z.array(z.object({
    language: z.string().min(1, 'Language is required'),
    proficiency: z.string().min(1, 'Proficiency level is required'),
  })).optional(),
});

type ResumeFormData = z.infer<typeof resumeSchema>;

const templates = [
  {
    id: 'modern',
    name: 'Modern',
    description: 'Clean and contemporary design with a focus on readability',
    image: 'https://images.pexels.com/photos/590016/pexels-photo-590016.jpeg',
    file: '/templates/my-template.pdf',
  },
  {
    id: 'simple',
    name: 'Simple',
    description: 'Minimalist layout that puts your content first',
    image: 'https://images.pexels.com/photos/590022/pexels-photo-590022.jpeg',
  },
  {
    id: 'creative',
    name: 'Creative',
    description: 'Stand out with a unique and colorful design',
    image: 'https://images.pexels.com/photos/5673488/pexels-photo-5673488.jpeg',
  },
  {
    id: 'classic',
    name: 'Classic',
    description: 'Traditional format trusted by professionals',
    image: 'https://images.pexels.com/photos/590016/pexels-photo-590016.jpeg',
  },
];

const CreateResume: React.FC = () => {
  const [selectedTemplate, setSelectedTemplate] = useState<string>('');
  const [currentStep, setCurrentStep] = useState(1);
  
  const { register, control, handleSubmit, watch, formState: { errors } } = useForm<ResumeFormData>({
    resolver: zodResolver(resumeSchema),
    defaultValues: {
      experience: [{ jobTitle: '', company: '', startDate: '', endDate: '', description: '' }],
      education: [{ degree: '', school: '', graduationDate: '', achievements: '' }],
      skills: { technical: [''], soft: [''] },
      certifications: [{ name: '', issuer: '', date: '' }],
      languages: [{ language: '', proficiency: '' }],
    },
  });

  const { fields: experienceFields, append: appendExperience, remove: removeExperience } = useFieldArray({
    control,
    name: 'experience',
  });

  const { fields: educationFields, append: appendEducation, remove: removeEducation } = useFieldArray({
    control,
    name: 'education',
  });

  const { fields: certificationFields, append: appendCertification, remove: removeCertification } = useFieldArray({
    control,
    name: 'certifications',
  });

  
  const onSubmit = async (data: ResumeFormData) => {
   

    console.log(data);
  
    const tpl = templates.find(t => t.id === selectedTemplate);
    if (!tpl?.file) {
      alert('Please select a template');
      return;
    }
  
    try {
      const arrayBuffer = await fetch(tpl.file).then(r => r.arrayBuffer());
      const pdfDoc = await PDFDocument.load(arrayBuffer);
      const helvetica = await pdfDoc.embedFont(StandardFonts.Helvetica);
  
      const page = pdfDoc.getPage(0);
  
      // 🖊️ Personal Info
      page.drawText(data.personalInfo.fullName, { x: 50, y: 700, size: 18, font: helvetica, color: rgb(0, 0, 0) });
      page.drawText(data.personalInfo.email,    { x: 50, y: 680, size: 12, font: helvetica });
      page.drawText(data.personalInfo.phone,    { x: 50, y: 665, size: 12, font: helvetica });
  
      // 🧑‍💼 Experience
      data.experience.forEach((exp, i) => {
        const y = 620 - i * 60;
        page.drawText(`${exp.jobTitle} @ ${exp.company}`, { x: 50, y, size: 12, font: helvetica });
        page.drawText(`${exp.startDate} – ${exp.endDate}`, { x: 300, y, size: 12, font: helvetica });
        page.drawText(exp.description, { x: 50, y: y - 14, size: 10, font: helvetica });
      });
  
      const pdfBytes = await pdfDoc.save();
      const blob = new Blob([pdfBytes], { type: 'application/pdf' });
  
      // 🧾 Download
      saveAs(blob, `${data.personalInfo.fullName}-Resume.pdf`);
    } catch (err) {
      console.error('PDF generation error:', err);
      alert('Failed to generate PDF. See console for details.');
    }
  };
  

  const nextStep = () => setCurrentStep(prev => prev + 1);
  const prevStep = () => setCurrentStep(prev => prev - 1);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.5 }}
      className="container mx-auto px-4 py-16 relative z-10"
    >
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-4 bg-gradient-to-r from-blue-400 to-purple-500 text-transparent bg-clip-text">
          Create Your Resume
        </h1>
        <p className="text-gray-300 text-center mb-12">
          Select a template and fill in your details to generate your personalized resume.
        </p>

        <div className="bg-gray-800 bg-opacity-70 rounded-xl p-8 backdrop-blur-sm border border-gray-700">
          {currentStep === 1 && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {templates.map((template) => (
                <div
                  key={template.id}
                  className={`relative rounded-lg overflow-hidden cursor-pointer transition-all duration-300 ${
                    selectedTemplate === template.id
                      ? 'ring-2 ring-blue-500 transform scale-[1.02]'
                      : 'hover:transform hover:scale-[1.02]'
                  }`}
                  onClick={() => setSelectedTemplate(template.id)}
                >
                  <img
                    src={template.image}
                    alt={template.name}
                    className="w-full h-48 object-cover"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-gray-900 to-transparent" />
                  <div className="absolute bottom-0 left-0 right-0 p-4">
                    <h3 className="text-xl font-semibold mb-1">{template.name}</h3>
                    <p className="text-sm text-gray-300">{template.description}</p>
                  </div>
                </div>
              ))}
            </div>
          )}

          

          {currentStep === 2 && (
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
              {/* Personal Information */}
              <div className="space-y-4">
                
                <h2 className="text-2xl font-semibold mb-4">Personal Information</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">
                      Full Name
                    </label>
                    <input
                      type="text"
                      {...register('personalInfo.fullName')}
                      className="w-full px-4 py-2 bg-gray-700 rounded-lg border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    {errors.personalInfo?.fullName && (
                      <p className="text-red-400 text-sm mt-1">
                        {errors.personalInfo.fullName.message}
                      </p>
                    )}
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-300 mb-1">
                      Email
                    </label>
                    <input
                      type="email"
                      {...register('personalInfo.email')}
                      className="w-full px-4 py-2 bg-gray-700 rounded-lg border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    {errors.personalInfo?.email && (
                      <p className="text-red-400 text-sm mt-1">
                        {errors.personalInfo.email.message}
                      </p>
                    )}
                  </div>
                </div>
              </div>

              {/* Work Experience */}
              <div className="space-y-4">
                <h2 className="text-2xl font-semibold mb-4">Work Experience</h2>
                {experienceFields.map((field, index) => (
                  <div key={field.id} className="p-4 bg-gray-700 rounded-lg space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-1">
                          Job Title
                        </label>
                        <input
                          type="text"
                          {...register(`experience.${index}.jobTitle`)}
                          className="w-full px-4 py-2 bg-gray-600 rounded-lg border border-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-300 mb-1">
                          Company
                        </label>
                        <input
                          type="text"
                          {...register(`experience.${index}.company`)}
                          className="w-full px-4 py-2 bg-gray-600 rounded-lg border border-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                      </div>
                    </div>
                    {index > 0 && (
                      <button
                        type="button"
                        onClick={() => removeExperience(index)}
                        className="text-red-400 hover:text-red-300 text-sm flex items-center"
                      >
                        <Minus className="w-4 h-4 mr-1" />
                        Remove Experience
                      </button>
                    )}
                  </div>
                ))}
                <button
                  type="button"
                  onClick={() => appendExperience({ jobTitle: '', company: '', startDate: '', endDate: '', description: '' })}
                  className="text-blue-400 hover:text-blue-300 text-sm flex items-center"
                >
                  <Plus className="w-4 h-4 mr-1" />
                  Add Experience
                </button>
              </div>

               {/* Education */}
<div className="space-y-4">
  <h2 className="text-2xl font-semibold mb-4">Education</h2>
  {educationFields.map((field, index) => (
    <div key={field.id} className="p-4 bg-gray-700 rounded-lg space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            Degree
          </label>
          <input
            type="text"
            {...register(`education.${index}.degree` as const)}
            className="w-full px-4 py-2 bg-gray-600 rounded-lg border border-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            School
          </label>
          <input
            type="text"
            {...register(`education.${index}.school` as const)}
            className="w-full px-4 py-2 bg-gray-600 rounded-lg border border-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            Graduation Date
          </label>
          <input
            type="date"
            {...register(`education.${index}.graduationDate` as const)}
            className="w-full px-4 py-2 bg-gray-600 rounded-lg border border-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            Achievements (optional)
          </label>
          <input
            type="text"
            {...register(`education.${index}.achievements` as const)}
            className="w-full px-4 py-2 bg-gray-600 rounded-lg border border-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>
      {index > 0 && (
        <button
          type="button"
          onClick={() => removeEducation(index)}
          className="text-red-400 hover:text-red-300 text-sm flex items-center"
        >
          <Minus className="w-4 h-4 mr-1" />
          Remove Education
        </button>
      )}
    </div>
  ))}
  <button
    type="button"
    onClick={() => appendEducation({ degree: '', school: '', graduationDate: '', achievements: '' })}
    className="text-blue-400 hover:text-blue-300 text-sm flex items-center"
  >
    <Plus className="w-4 h-4 mr-1" />
    Add Education
  </button>
</div>

{/* Certifications */}
<div className="space-y-4 mt-8">
  <h2 className="text-2xl font-semibold mb-4">Certifications</h2>
  {certificationFields.map((field, index) => (
    <div key={field.id} className="p-4 bg-gray-700 rounded-lg space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            Certification Name
          </label>
          <input
            type="text"
            {...register(`certifications.${index}.name` as const)}
            className="w-full px-4 py-2 bg-gray-600 rounded-lg border border-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            Issuing Organization
          </label>
          <input
            type="text"
            {...register(`certifications.${index}.issuer` as const)}
            className="w-full px-4 py-2 bg-gray-600 rounded-lg border border-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-1">
          Date of Issue
        </label>
        <input
          type="date"
          {...register(`certifications.${index}.date` as const)}
          className="w-full px-4 py-2 bg-gray-600 rounded-lg border border-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      {index > 0 && (
        <button
          type="button"
          onClick={() => removeCertification(index)}
          className="text-red-400 hover:text-red-300 text-sm flex items-center"
        >
          <Minus className="w-4 h-4 mr-1" />
          Remove Certification
        </button>
      )}
    </div>
  ))}
  <button
    type="button"
    onClick={() => appendCertification({ name: '', issuer: '', date: '' })}
    className="text-blue-400 hover:text-blue-300 text-sm flex items-center"
  >
    <Plus className="w-4 h-4 mr-1" />
    Add Certification
  </button>
</div>
 
              {/* Preview and Download Buttons */}
              <div className="flex justify-between pt-8">
                <button
                  type="button"
                  onClick={() => prevStep()}
                  className="px-6 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors"
                >
                  Back
                </button>
                <div className="space-x-4">
                  <button
                    type="button"
                    className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-500 transition-colors flex items-center"
                  >
                    <Eye className="w-4 h-4 mr-2" />
                    Preview
                  </button>
                  <button
                    type="submit"
                    className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-500 transition-colors flex items-center"
                  >
                    
                    <Download className="w-4 h-4 mr-2" />
                    Download
                  </button>
                </div>
              </div>
            </form>
          )}

          {currentStep === 1 && (
            <div className="mt-8 flex justify-end">
              <button
                onClick={nextStep}
                disabled={!selectedTemplate}
                className={`px-6 py-2 rounded-lg font-medium transition-colors ${
                  selectedTemplate
                    ? 'bg-blue-600 hover:bg-blue-500 text-white'
                    : 'bg-gray-700 text-gray-400 cursor-not-allowed'
                }`}
              >
                Next Step
              </button>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default CreateResume;