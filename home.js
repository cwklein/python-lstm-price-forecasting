import React from 'react'

import projectStyles from '.style.module.css'
import styles from './home.module.css'

const Home = (props) => {
  return (
    <div className={styles['container']}>
      <div className={styles['hero']}>
        <div className={styles['container1']}>
          <h1 className={styles['text']}>Stock Price Predictor</h1>
          <span className={styles['text1']}>
            <span>
              <span>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non
                volutpat turpis.
                <span
                  dangerouslySetInnerHTML={{
                    __html: ' ',
                  }}
                />
              </span>
              <span>
                <span
                  dangerouslySetInnerHTML={{
                    __html: ' ',
                  }}
                />
              </span>
            </span>
            <span>
              <span>
                Mauris luctus rutrum mi ut rhoncus. Integer in dignissim tortor.
                <span
                  dangerouslySetInnerHTML={{
                    __html: ' ',
                  }}
                />
              </span>
              <span>
                <span
                  dangerouslySetInnerHTML={{
                    __html: ' ',
                  }}
                />
              </span>
            </span>
          </span>
          <form className={styles['form']}>
            <select required className={styles['select']}>
              <option selected>Select a company..</option>
              <option value="AAPL">Apple</option>
              <option value="AMZN">Amazon</option>
            </select>
            <button
              type="button"
              className={` ${styles['button']} ${projectStyles['button']} `}
            >
              Button
            </button>
          </form>
          <div className={styles['btn-group']}></div>
        </div>
        <img
          alt="image"
          src="https://images.unsplash.com/photo-1525498128493-380d1990a112?ixid=Mnw5MTMyMXwwfDF8c2VhcmNofDI0fHxtaW5pbWFsaXNtJTIwZ3JlZW58ZW58MHx8fHwxNjI1ODQxMDcw&amp;ixlib=rb-1.2.1&amp;w=1200"
          className={styles['image']}
        />
      </div>
    </div>
  )
}

export default Home
